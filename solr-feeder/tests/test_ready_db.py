from .support_db import select


def test_db_ready(db):
    select(db, table='namex.solr_dataimport_names_vw')
    select(db, table='namex.solr_dataimport_conflicts_vw')
    select(db, table='solr_feeder')
