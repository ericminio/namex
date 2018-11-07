from flask import jsonify, request
from flask_restplus import Resource, Namespace
import requests
import json

api = Namespace('exactMatchMeta', description='Exact Match System - Metadata')
import os
SOLR_URL = os.getenv('SOLR_BASE_URL')


@api.route("")
class ExactMatch(Resource):

    @staticmethod
    def get():
        query = request.args.get('query')
        url = SOLR_URL + '/solr/possible.conflicts' + \
              '/select?' + \
              'sow=false' + \
              '&df=name_exact_match' + \
              '&wt=json' + \
              '&q=' + query
        results = requests.get(url)
        text = results.text
        answer = json.loads(text)
        docs = answer['response']['docs']
        names =[{ 'name':doc['name'] } for doc in docs ]

        return jsonify({ 'names':names })
