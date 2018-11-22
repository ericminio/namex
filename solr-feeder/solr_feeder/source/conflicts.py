def select_all_conflicts_nrs(db):
    records = db.engine.execute("select nr_num from solr_feeder where solr_core='C' and status<>'C'").fetchall()
    return [record['nr_num'] for record in records]


def select_name_by_conflict_nr(db, nr):
    return db.engine.execute(
        "select NAME from namex.solr_dataimport_conflicts_vw where id='{}'".format(nr))\
        .fetchone()['name']
