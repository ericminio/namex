def select(db, table):
    result = db.engine.execute('select * from {}'.format(table)).fetchall()
    assert [] == result

def run(db, sqls):
    for sql in sqls:
        db.engine.execute(sql)


def seed_conflicts(db, name, nr, status='P'):
    run(db, [
        "insert into solr_feeder(nr_num, solr_core, status) values('{}', 'C', '{}');".format(nr, status),
        "insert into namex.solr_dataimport_conflicts_vw(ID, NAME) values('{}', '{}');".format(nr, name)
    ])


def seed_names(db, name, nr, status='P'):
    run(db, [
        "insert into solr_feeder(nr_num, solr_core, status) values('{}', 'N', '{}');".format(nr, status),
        "insert into namex.solr_dataimport_names_vw(nr_num, NAME) values('{}', '{}');".format(nr, name)
    ])


def read_all_seeds(db):
    return [{
        'nr_num': seed['nr_num'],
        'status': seed['status']
    } for seed in db.engine.execute(
        "select nr_num, status from solr_feeder").fetchall()]
