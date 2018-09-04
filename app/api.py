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


class Register(Resource):
    def post(self):
        name = request.get_json()['name' ]
        email = request.get_json()['email']
        username = request.get_json()['username']
        password = request.get_json()['password']

        cur.execute(
            "INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
            (name,
             email,
             username,
             password))

        conn.commit()

        # Close Connection
        cur.close()
        success = 'Sucessfully registered you may now log in with your username and password'
        return jsonify ({ 'message': success })



api.add_resource(Home, '/api/v1/', endpoint = 'homepage')
if __name__ == '__main__':
    app.run(debug=True)
