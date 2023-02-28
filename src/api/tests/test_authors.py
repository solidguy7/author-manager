import json
import unittest
from io import BytesIO
from flask_jwt_extended import create_access_token
from api.utils.test_base import BaseTestCase
from api.authors.models import Author
from api.books.models import Book

def create_authors():
    author1 = Author(first_name='John', last_name='Doe').create()
    Book(title="Test Book 1", year=1976, author_id=author1.id).create()
    Book(title="Test Book 2", year=1992, author_id=author1.id).create()
    author2 = Author(first_name='Jane', last_name='Doe').create()
    Book(title="Test Book 3", year=1986, author_id=author2.id).create()
    Book(title="Test Book 4", year=1992, author_id=author2.id).create()

def login():
    access_token = create_access_token(identity='kunal.relan@hotmail.com')
    return access_token

class TestAuthors(BaseTestCase):
    def setUp(self) -> None:
        super(TestAuthors, self).setUp()
        create_authors()

    def test_create_author(self):
        token = login()
        author = {
            'first_name': 'Johny',
            'last_name': 'Doee'
        }
        response = self.app.post('/api/authors/', data=json.dumps(author), content_type='application/json',
                                 headers={'Authorization': 'Bearer ' + token})
        data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertTrue('author' in data)

    def test_create_author_no_authorization(self):
        author = {
            'first_name': 'Johny',
            'last_name': 'Doee'
        }
        response = self.app.post('/api/authors/', data=json.dumps(author), content_type='application/json')
        self.assertEqual(401, response.status_code)

    def test_create_author_no_name(self):
        token = login()
        author = {
            'first_name': 'Johny'
        }
        response = self.app.post('/api/authors/', data=json.dumps(author), content_type='application/json',
                                 headers={'Authorization': 'Bearer ' + token})
        self.assertEqual(422, response.status_code)

    def test_upload_avatar(self):
        token = login()
        response = self.app.post('/api/authors/avatar/2', data=dict(avatar=(BytesIO(b'test'), 'test_file.jpg')),
                                 content_type='multipart/form-data', headers={'Authorization': 'Bearer ' + token})
        self.assertEqual(200, response.status_code)

    def test_upload_avatar_with_csv_file(self):
        token = login()
        response = self.app.post('/api/authors/avatar/2', data=dict(file=(BytesIO(b'test'), 'test_file.csv')),
                                 content_type='multipart/form-data', headers={'Authorization': 'Bearer ' + token})
        self.assertEqual(422, response.status_code)

    def test_get_authors(self):
        response = self.app.get('/api/authors/', content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('authors' in data)

    def test_get_author_detail(self):
        response = self.app.get('/api/authors/2', content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('author' in data)

    def test_update_author(self):
        token = login()
        author = {
            'first_name': 'Joseph',
            'last_name': 'Doee'
        }
        response = self.app.put('/api/authors/2', data=json.dumps(author), content_type='application/json',
                                headers={'Authorization': 'Bearer ' + token})
        self.assertEqual(200, response.status_code)

    def test_delete_author(self):
        token = login()
        response = self.app.delete('/api/authors/2', headers={'Authorization': 'Bearer ' + token})
        self.assertEqual(204, response.status_code)

    def test_create_book(self):
        token = login()
        book = {
            'title': 'Alice in wonderland',
            'year': 1982,
            'author_id': 2
        }
        response = self.app.post('/api/books/', data=json.dumps(book), content_type='application/json',
                                 headers={'Authorization': 'Bearer ' + token})
        data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertTrue('book' in data)

    def test_create_book_no_author(self):
        token = login()
        book = {
            'title': 'Alice in wonderland',
            'year': 1982
        }
        response = self.app.post('/api/books/', data=json.dumps(book), content_type='application/json',
                                 headers={'Authorization': 'Bearer ' + token})
        self.assertEqual(422, response.status_code)

    def test_create_book_no_authorization(self):
        book = {
            'title': 'Alice in wonderland',
            'year': 1982,
            'author_id': 2
        }
        response = self.app.post('/api/books/', data=json.dumps(book), content_type='application/json')
        self.assertEqual(401, response.status_code)

    def test_get_books(self):
        response = self.app.get('/api/books/', content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('books' in data)

    def test_get_book_detail(self):
        response = self.app.get('/api/books/2', content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertTrue('book' in data)

    def test_update_book(self):
        token = login()
        book = {
            'year': 1992,
            'title': 'Alice'
        }
        response = self.app.put('/api/books/2', data=json.dumps(book), content_type='application/json',
                                headers={'Authorization': 'Bearer ' + token})
        self.assertEqual(200, response.status_code)

    def test_delete_book(self):
        token = login()
        response = self.app.delete('/api/books/2', headers={'Authorization': 'Bearer ' + token})
        self.assertEqual(204, response.status_code)

if __name__ == '__main__':
    unittest.main()
