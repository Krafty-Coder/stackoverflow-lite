from flask import Flask, jsonify, request, session
from flask_restful import Resource, Api
from app.models import *
from flask_httpauth import HTTPBasicAuth
from passlib.hash import sha256_crypt


app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


class Home(Resource):
    '''Api for the homepage'''
    def get(self):
        '''method for getting the homepage'''
        return jsonify({'message': 'Stackoverflow-lite, the alternate app if they get to hack Stackoverflow *.* '})


api.add_resource(Home, '/api/v1/', endpoint = 'homepage')
if __name__ == '__main__':
    app.run(debug=True)
