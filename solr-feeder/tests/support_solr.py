import requests
import json


def ping(solr, core):
    r = requests.get(solr + core + '/admin/ping')
    assert r.status_code == 200


def read_all_possible_conflicts(solr):
    url = solr + '/possible.conflicts' + \
          '/select?' + \
          'sow=false' + \
          '&wt=json' + \
          '&q=*'
    response = requests.get(url)
    assert response.status_code == 200

    answer = json.loads(response.text)
    return [{'name': doc['name']} for doc in answer['response']['docs']]


def read_all_names(solr):
    url = solr + '/names' + \
          '/select?' + \
          'sow=false' + \
          '&wt=json' + \
          '&q=*'
    response = requests.get(url)
    assert response.status_code == 200

    answer = json.loads(response.text)
    return [{'name': doc['name']} for doc in answer['response']['docs']]