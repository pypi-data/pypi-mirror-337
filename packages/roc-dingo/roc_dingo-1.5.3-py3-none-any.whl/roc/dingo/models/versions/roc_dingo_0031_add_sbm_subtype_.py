# -*- coding: utf-8 -*-
"""empty message

Revision ID: roc_dingo_0031_add_sbm_subtype
Revises: roc_dingo_0030_add_packet_acq_time
Create Date: 2024-04-25 10:44:55.787939

"""

from alembic import op
import sqlalchemy as sa

from poppy.pop.alembic.helpers import execute, user

# revision identifiers, used by Alembic.
revision = "roc_dingo_0031_add_sbm_subtype"
down_revision = "roc_dingo_0030_add_packet_acq_time"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "sbm_log",
        sa.Column("sbm_subtype", sa.String(), nullable=True),
        schema="pipeline",
    )

    # fix table permissions
    grant_user_perm = """GRANT SELECT, INSERT, UPDATE
        ON ALL TABLES IN SCHEMA pipeline TO {0}""".format(user)
    execute(grant_user_perm)
    # Make sure admin can reset event_log_id_seq
    # alter_seq_admin = (
    #    """ALTER SEQUENCE IF EXISTS event_log_id_seq
    #    OWNER TO {0}""".format(admin)
    # )
    # execute(alter_seq_admin)
    # Fix sequence permissions
    grant_user_seq = """GRANT USAGE, SELECT
        ON ALL SEQUENCES IN SCHEMA pipeline TO {0}""".format(user)
    execute(grant_user_seq)


def downgrade():
    op.drop_column("sbm_log", "sbm_subtype", schema="pipeline")

    # fix table permissions
    grant_user_perm = """GRANT SELECT, INSERT, UPDATE
        ON ALL TABLES IN SCHEMA pipeline TO {0}""".format(user)
    execute(grant_user_perm)
    # Make sure admin can reset event_log_id_seq
    # alter_seq_admin = (
    #    """ALTER SEQUENCE IF EXISTS event_log_id_seq
    #    OWNER TO {0}""".format(admin)
    # )
    # execute(alter_seq_admin)
    # Fix sequence permissions
    grant_user_seq = """GRANT USAGE, SELECT
        ON ALL SEQUENCES IN SCHEMA pipeline TO {0}""".format(user)
    execute(grant_user_seq)
