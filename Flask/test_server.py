import unittest
from flask_testing import TestCase
from server import app, TinyDB
import json

class ServerTest(TestCase):
    TESTING = True

    def create_app(self):
        app.config['TESTING'] = True
        app.config['DATABASE_FILE'] = 'test_db.json'
        return app

    def setUp(self):
        self.db = TinyDB(app.config['DATABASE_FILE'])
        self.db.truncate()

    def tearDown(self):
        self.db.truncate()

    def test_login(self):
        response = self.client.post('/login/', data=json.dumps({"username": "admin", "password": "admin"}), content_type='application/json')
        self.assert200(response)
        self.assertEqual(response.json, {"message": "Hello, admin!"})

    def test_login_fail(self):
        response = self.client.post('/login/', data=json.dumps({"username": "admin", "password": "wrong"}), content_type='application/json')
        self.assert401(response)
        self.assertEqual(response.json, {"message": "Invalid credentials"})

    def test_upload_image_without_file(self):
        response = self.client.post('/upload_image/')
        self.assert400(response)
if __name__ == '__main__':
    unittest.main()
