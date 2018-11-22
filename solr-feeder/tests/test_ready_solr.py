from .support_solr import ping


def test_solr_ready(solr):
    ping(solr, '/possible.conflicts')
    ping(solr, '/names')
