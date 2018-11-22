def update_status_to_completed(db, nr):
    db.engine.execute("update solr_feeder set status='C' where nr_num='{}'".format(nr))
