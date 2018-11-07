from flask import jsonify
from flask_restplus import Resource, Namespace
import requests
import json

api = Namespace('exactMatchMeta', description='Exact Match System - Metadata')


@api.route("")
class ExactMatch(Resource):

    @staticmethod
    def get():
        url = 'http://localhost:8983/solr/exact_match/select?q=*:*&wt=json'
        results = requests.get(url)
        text = results.text
        answer = json.loads(text)
        docs = answer['response']['docs']
        names =[{ 'name':doc['name'] } for doc in docs ]

        return jsonify({ 'names':names })
