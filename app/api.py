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



class AllQuestionsAPI(Resource):
    '''Api for the questions posted'''
    def post(self):
        '''API method for creating a question'''
        title = request.get_json()['title']
        description = request.get_json()['description']
        if title and description:
            cur.execute(
                "INSERT INTO questions(title, description) VALUES(%s, %s)",
                (title,
                 description))
            conn.commit()
            success = 'Your question was successfully added into the database'
            return jsonify({'message': success})
        else:
            error = 'Please input content into your title and description field'
            return jsonify({'message': error})



api.add_resource(Home, '/api/v1/', endpoint = 'homepage')
if __name__ == '__main__':
    app.run(debug=True)
