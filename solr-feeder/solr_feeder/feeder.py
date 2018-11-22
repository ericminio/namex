from solr_feeder.source.conflicts import select_all_conflicts_nrs, select_name_by_conflict_nr
from solr_feeder.source import update_status_to_completed
from solr_feeder.target import post_solr_conflict


class Feeder:

    def __init__(self, db, solr):
        self.db = db
        self.solr = solr

    def go(self):
        for nr in select_all_conflicts_nrs(self.db):
            name = select_name_by_conflict_nr(self.db, nr)
            post_solr_conflict(self.solr, nr, name)
            update_status_to_completed(self.db, nr)
