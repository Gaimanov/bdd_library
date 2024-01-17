import unittest

from faker import Faker
from flask import json

from libraries.library_app import app, library


class LibraryTestCase(unittest.TestCase):  # Ran 4 tests in 0.245s

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.faker = Faker()

    def test_add_book(self):
        book_tittle = self.faker.word()
        response = self.app.post('/add_book', json={'title': book_tittle})
        self.assertEqual(response.status_code, 201)
        self.assertIn(book_tittle, library.available_books())

    def test_borrow_book(self):
        book_tittle = self.faker.word()
        # add a book
        self.app.post('/add_book', json={'title': book_tittle})
        # borrow the book
        response = self.app.post('/borrow_book', json={'title': book_tittle})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(book_tittle, library.available_books())

    def test_return_book(self):
        book_tittle = self.faker.word()
        # Add and borrow a book
        self.app.post('/add_book', json={'title': book_tittle})
        self.app.post('/borrow_book', json={'title': book_tittle})
        # return the book
        response = self.app.post('/return_book', json={'title': book_tittle})
        self.assertEqual(response.status_code, 200)
        self.assertIn(book_tittle, library.available_books())

    def test_available_books(self):
        book_tittle = self.faker.word()
        self.app.post('/add_book', json={'title': book_tittle})
        response = self.app.get('/available_books')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(book_tittle, data)
