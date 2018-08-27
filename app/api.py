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


class AllQuestionsAPI(Resource):
    '''Api for creating the questions'''
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

    '''Api for the questions posted'''
    def get(self):
        result = cur.execute("SELECT * FROM questions;")
        questions = cur.fetchall()

        if questions:
            return jsonify(questions)
        else:
            error = 'No questions in the database'
            return {'message': error}


class QuestionAPI(Resource):
    # decorators  = [auth.login_required]
    '''Api for getting a particular question'''
    def get(self, id):
        '''API method for getting a question'''
        cur.execute('SELECT * FROM questions WHERE id={}'.format(id))
        question = cur.fetchone()
        # cur.close()
        if question:
            return jsonify(question)
        else:
            error = "No question with that id exists"
            return jsonify({"message": error})

    def put(self, id):
        '''API method for updating a question'''
        cur.execute("SELECT * FROM articles WHERE id = {}".format(id))
        question =  cur.fetchone()
        title = request.get_json()['title']
        description = request.get_json()['description']
        cur.execute(
            "UPDATE question SET title={}, description={} WHERE id={}".format(
                title, description, id))
        conn.commit()
        success = 'Question updated successfully'
        return jsonify({'message': success})

    def delete(self, id):
        '''API method for deleting a question'''
        cur.execute("DELETE FROM questions WHERE id = {}".format(id))
        conn.commit()
        success = 'Deleted the question successfully'
        return {'message': success}


api.add_resource(Home, '/api/v1/', endpoint = 'homepage')
api.add_resource(AllQuestionsAPI, '/api/v1/questions', endpoint = 'questions')
api.add_resource(QuestionAPI, '/api/v1/questions/<int:id>', endpoint='question')
api.add_resource(AllAnswersAPI, '/api/v1/answers/', endpoint = 'answers')
api.add_resource(AnswerAPI, '/api/v1/answer/<int:id>', endpoint = 'answer')
api.add_resource(Register, '/api/v1/auth/register')
api.add_resource(Login, '/api/v1/auth/login')
if __name__ == '__main__':
    app.run(debug=True)


