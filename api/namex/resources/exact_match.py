from flask import jsonify
from flask_restplus import Resource, Namespace

api = Namespace('exactMatchMeta', description='Exact Match System - Metadata')


@api.route("")
class ExactMatch(Resource):

    @staticmethod
    def get():
        return jsonify({ 'names':[
            {'name': 'JM Van Damme Ltd'}
        ] })
