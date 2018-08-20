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


class Login(Resource):
    def post(self):
        username = request.get_json()['username']
        password_candidate = request.get_json()['password']

        result = cur.execute(
            "SELECT * FROM users WHERE username = %s",
            [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            cur.close()
            if sha256_crypt.verify(password_candidate, password):
                # Password and username matches
                session['logged_in'] = True
                session['username'] = username
                success = 'Successfully logged in'
                return {'message': success}

            else:
                error = 'Password or username incorrect, Invalid login'
                return {'message': error}
        else:
            error = "Username not found"
            return {'message': error}


api.add_resource(Home, '/api/v1/', endpoint = 'homepage')
if __name__ == '__main__':
    app.run(debug=True)
