#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Contains dingo tasks to update utc times (computed with SPICE kernels)
into the ROC database."""

from datetime import datetime, timedelta
from pathlib import Path
import uuid

from sqlalchemy import and_, true

from poppy.core.logger import logger
from poppy.core.db.connector import Connector
from poppy.core.task import Task

from roc.dingo.constants import (
    PIPELINE_DATABASE,
    TRYOUTS,
    TIME_WAIT_SEC,
    SQL_LIMIT,
    NAIF_SOLO_ID,
)
from roc.dingo.models.data import SbmLog, BiaSweepLog, LfrKcoeffDump
from roc.dingo.models.packet import TmLog
from roc.dingo.tools import query_db, is_sclk_uptodate, valid_time, load_spice


class UpdateUtcTime(Task):
    """
    Update UTC times in the
    in ROC database
    """

    plugin_name = "roc.dingo"
    name = "update_utc_time"

    def add_targets(self):
        pass

    @Connector.if_connected(PIPELINE_DATABASE)
    def setup_inputs(self):
        # Get SOLO SPICE kernels (SCLK and LSK)
        self.sclk_file = self.pipeline.get("sclk", default=[None], create=True)[0]
        if not self.sclk_file:
            raise FileNotFoundError(
                f"sclk_file input file is missing!\t[{self.job_id}]"
            )
        self.lsk_file = self.pipeline.get("lsk", default=[None], create=True)[0]
        if not self.sclk_file or not self.lsk_file:
            raise FileNotFoundError(
                f"lsk_file input file is missing!\t[{self.job_id}]"
            )
        self.spice = load_spice([self.lsk_file, self.sclk_file])

        # Get start_time input value
        self.start_time = valid_time(
            self.pipeline.get("start_time", default=[None])[0],
        )

        # Get end_time input value
        self.end_time = valid_time(
            self.pipeline.get("end_time", default=[None])[0],
        )

        # get a database session
        self.session = Connector.manager[PIPELINE_DATABASE].session

        # Get tryouts from pipeline properties
        self.tryouts = self.pipeline.get("tryouts", default=[TRYOUTS], create=True)[0]

        # Get wait from pipeline properties
        self.wait = self.pipeline.get("wait", default=[TIME_WAIT_SEC], create=True)[0]

        # Retrieve --limit keyword value
        self.limit = self.pipeline.get("limit", default=[SQL_LIMIT], args=True)[0]

        # Database insertion datetime
        self.insert_time = datetime.today()

    def run(self):
        # Define task job ID (long and short)
        self.job_uuid = str(uuid.uuid4())
        self.job_id = self.job_uuid[:8]
        logger.info(f"Task {self.job_id} is starting")
        try:
            self.setup_inputs()
        except Exception:
            logger.exception(f"Initializing inputs has failed for task {self.job_id}!")
            self.pipeline.exit()
            return

        # List of tables for which utc times must be updated
        table_list = [TmLog, SbmLog, BiaSweepLog, LfrKcoeffDump]

        # Loop over tables
        for current_table in table_list:
            # Retrieve table rows which are flagged as predictive in the table
            filters = [current_table.utc_time_is_predictive == true()]
            if self.start_time:
                filters.append(current_table.utc_time >= str(self.start_time))
            if self.end_time:
                filters.append(current_table.utc_time < str(self.end_time))
            filters = and_(*filters)
            rows = query_db(
                self.session,
                current_table,
                filters=filters,
                tryouts=self.tryouts,
                wait=self.wait,
                limit=self.limit,
                raw=True,
            )

            n_rows = len(rows)
            logger.info(
                f"{n_rows} predictive time(s) for {current_table.__tablename__} between {self.start_time} and {self.end_time}\t[{self.job_id}]"
            )
            if n_rows == 0:
                continue

            # Check/Update utc time
            updated_rows = [
                current_row for current_row in rows if self.update_time(current_row)
            ]
            n_rows = len(updated_rows)

            if n_rows > 0:
                # Then commit changes in database
                self.session.commit()
                logger.info(
                    f"{n_rows} updated in {current_table.__tablename__}\t[{self.job_id}]"
                )
            else:
                logger.info(
                    f"No data to update in {current_table.__tablename__}\t[{self.job_id}]"
                )

    def update_time(self, row, naif_id=NAIF_SOLO_ID):
        """
        Check if utc_time in the input row is up-to-date.
        If not, then update it using SPICE.

        :param row: input table row to check/update (dictionary)
        :return:True if row has been updated, False otherwise
        """
        is_uptodate = False
        if is_sclk_uptodate(
            row.utc_time + timedelta(days=1), Path(self.sclk_file).name
        ):
            if hasattr(row, 'cuc_time'):
                cuc_time = row.cuc_time
            else:
                cuc_time = str(row.cuc_coarse_time) + ":" + str(row.cuc_fine_time)

            row.utc_time = self.spice.obt2utc(naif_id, cuc_time)
            row.utc_time_is_predictive = False
            row.insert_time = self.insert_time
            logger.debug(f"{row.id} has been updated [{self.job_id}]")
            is_uptodate = True

        return is_uptodate
