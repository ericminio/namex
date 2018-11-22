import requests


def post_solr_conflict(solr, nr, name):
    url, headers, data = solr_conflict(solr, nr, name)
    requests.post(url, headers=headers, data=data)


def solr_conflict(solr, nr, name):
    url = solr + '/possible.conflicts/update?commit=true'
    headers = {'content-type': 'application/json'}
    data = '[{"source":"CORP", "name":"' + name + '", "id":"' + nr + '"}]'
    return url, headers, data
