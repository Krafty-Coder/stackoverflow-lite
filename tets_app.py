import unittest
from app import *

class QuestionTestCase(unittest.TestCase):
    """Testing Questions CRUD"""
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

    def test_the_get_question_api(self):
        response = self.client().get('api/v1/questions', content_type='aplication/json')
        self.assertEqual(response.status_code, 200)


    def test_create_question(self):
        """Method tests post method on the question"""
        response = self.client().post('/api/v1/questions', content_type='application/json')
        self.assertEqual(response.status_code, 400)


    def test_retrieve_all_questions(self):
        """Method tests getting all questions"""
        response = self.client().get('/api/v1/questions')
        self.assertEqual(response.status_code, 200)

class TestHomePage(unittest.TestCase):
    """Just one method for testing the home page"""
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

    def test_home_page_api(self):
        response = self.client().get('api/v1/', content_type='aplication/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Stackoverflow-lite, the alternate app if they get to hack Stackoverflow *.* ', response.data)

    def test_getting_single_question(self):
        """Method tests for getting a single question"""
        response = self.client().get('api/v1/questions/1')
        self.assertEqual(response.status_code, 200)

