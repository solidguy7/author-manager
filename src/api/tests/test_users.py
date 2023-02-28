import json
import unittest
from api.users.models import User
from api.utils.test_base import BaseTestCase
from api.utils.token import generate_verification_token

def create_users():
    user1 = User(email='kunal.relan12@gmail.com',
                 username='kunalrelan12',
                 password=User.generate_hash('helloworld'),
                 isVerified=True).create()
    user2 = User(email='kunal.relan123@gmail.com',
                 username='kunalrelan125',
                 password=User.generate_hash('helloworld')).create()

class TestUsers(BaseTestCase):
    def setUp(self):
        super(TestUsers, self).setUp()
        create_users()

    def test_login_user(self):
        user = {
            "email": "kunal.relan12@gmail.com",
            "password": "helloworld"
        }
        response = self.app.post('/api/users/login', data=json.dumps(user), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertTrue('access_token' in data)

    def test_login_user_wrong_credentials(self):
        user = {
            "email": "kunal.relan12@gmail.com",
            "password": "helloworld12"
        }
        response = self.app.post('api/users/login', data=json.dumps(user), content_type='application/json')
        self.assertEqual(403, response.status_code)

    def test_login_unverified_user(self):
        user = {
            "email": "kunal.relan123@gmail.com",
            "password": "helloworld"
        }
        response = self.app.post('api/users/login', data=json.dumps(user), content_type='application/json')
        self.assertEqual(400, response.status_code)

    def test_create_user(self):
        user = {
            "email": "kunal.relan12345@gmail.com",
            "password": "helloworld12345",
            "username": "kunalrelan12345"
        }
        response = self.app.post('api/users/', data=json.dumps(user), content_type='application/json')
        self.assertEqual(201, response.status_code)

    def test_create_user_without_username(self):
        user = {
            "password": "helloworld",
            "email": "kunal.relan12@gmail.com"
        }
        response = self.app.post('api/users/', data=json.dumps(user), content_type='application/json')
        self.assertEqual(422, response.status_code)

    def test_confirm_email(self):
        token = generate_verification_token('kunal.relan123@gmail.com')
        response = self.app.get('/api/users/confirm/' + token)
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('success' in data['code'])

    def test_confirm_email_for_verified_user(self):
        token = generate_verification_token('kunal.relan12@gmail.com')
        response = self.app.get('/api/users/confirm/' + token)
        self.assertEqual(422, response.status_code)

    def test_confirm_email_with_incorrect_email(self):
        token = generate_verification_token('kunal.relan43@gmail.com')
        response = self.app.get('/api/users/confirm/' + token)
        self.assertEqual(404, response.status_code)

if __name__ == '__main__':
    unittest.main()