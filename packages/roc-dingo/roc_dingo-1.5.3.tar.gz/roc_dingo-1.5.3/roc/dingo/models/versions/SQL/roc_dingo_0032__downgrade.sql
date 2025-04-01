DELETE FROM
  pipeline.bia_sweep_log T USING pipeline.bia_sweep_log D
  WHERE T.utc_time = D.utc_time AND T.sweep_step = D.sweep_step AND
        T.insert_time < D.insert_time;

DELETE FROM
  pipeline.lfr_kcoeff_dump T USING pipeline.lfr_kcoeff_dump D
  WHERE T.utc_time = D.utc_time AND T.kcoeff_pkt_nr = D.kcoeff_pkt_nr AND
        T.insert_time < D.insert_time;
        