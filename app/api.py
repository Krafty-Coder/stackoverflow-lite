from flask import Flask, jsonify, request, session
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from app.models import cur, conn
from flask_httpauth import HTTPBasicAuth
from passlib.hash import sha256_crypt


app = Flask(__name__)
api = Api(app)
CORS(api)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
auth = HTTPBasicAuth()


class Home(Resource):
    '''Api for the homepage'''
    @app.route('/api/v1')
    @cross_origin()
    def get(self):
        '''method for getting the homepage'''
        return jsonify({'message': 'Stackoverflow-lite, the alternate app if they get to hack Stackoverflow *.* '})


class Register(Resource):
    @app.route('/api/v1/register')
    @cross_origin()
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
    @app.route('/api/v1/login')
    @cross_origin()
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
    '''Api for the questions posted'''
    @app.route('/api/v1/questions/')
    @cross_origin()
    def get(self):
        result = cur.execute("SELECT * FROM questions;")
        questions = cur.fetchall()

        if questions:
            return jsonify(questions)
        else:
            error = 'No questions in the database'
            return {'message': error}


    @app.route('/api/v1/questions')
    @cross_origin()
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


class QuestionAPI(Resource):
    # decorators  = [auth.login_required]
    '''Api for getting a particular question'''
    @app.route('/api/v1/questions')
    @cross_origin()
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

    @app.route('/api/v1/questions/<int:id>')
    @cross_origin()
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

    @app.route('/api/v1/questions/<int:id>')
    @cross_origin()
    def delete(self, id):
        '''API method for deleting a question'''
        cur.execute("DELETE FROM questions WHERE id = {}".format(id))
        conn.commit()
        success = 'Deleted the question successfully'
        return {'message': success}


class AllAnswersAPI(Resource):
    '''Api for the answers given to a particular question'''
    @app.route('/api/v1/answers')
    @cross_origin()
    def get(self, id):
        cur.execute('SELECT * FROM answers WHERE id={}'.format(id))
        result = cur.fetchone()
        result = result
        success = 'answers to the answers are the following'
        return jsonify ({'message': success}, { result } )


class AnswerAPI(Resource):
    decorators  = [auth.login_required]
    '''Api for getting a particular answer to a question'''
    @app.route('/api/v1/answers/<int:id>/')
    @cross_origin()
    def get(self, id):
        '''API method for getting an answer'''
        cur.execute('SELECT * FROM answers WHERE id={}'.format(id))
        answer = cur.fetchone()
        success = 'Answer retrived successfully'
        return jsonify ({'message': success}, { answer })

    @app.route('/api/v1/answers/<int:id>')
    @cross_origin()
    def put(self, id):
        '''API method for updating an answer'''
        cur.execute('SELECT * FROM answers WHERE id = {}'.format(id))
        result = cur.fetchone()
        title = request.get_json()['title']
        description = request.get_json()['description']
        cur.execute(
            "UPDATE answer SET title={}, description={} WHERE id={}".format(
                title, description, id))
        conn.commit()
        success = 'Successfully edited your answer'
        return { 'message': success }

    @app.route('/api/v1/answers/<int:id>/')
    @cross_origin()
    def delete(self, id):
        '''API method for deleting an answer'''
        cur.execute('DELETE FROM answers WHERE id = {}'.format(id))
        conn.commit()
        success = 'Successfully deleted your answer'
        return { 'message': success }



class AllCommentsAPI(Resource):
    '''Api for the comments posted per post'''
    @app.route('/api/v1/comments')
    @cross_origin()
    def get(self, id):
        pass


class CommentAPI(Resource):
    decorators  = [auth.login_required]
    '''Api for getting a particular comment to an answer of a question'''
    @app.route('/api/v1comment')
    @cross_origin()
    def get(self, id):
        '''API method for getting a comment'''
        pass

    @app.route('/api/v1/comment/<int:id>/')
    @cross_origin()
    def put(self, id):
        '''API method for updating a comment'''
        pass

    @app.route('/api/v1/comment/<int:id>/')
    @cross_origin()
    def delete(self, id):
        '''API method for deleting a comment'''
        pass


if __name__ == '__main__':
    app.run(debug=True)

