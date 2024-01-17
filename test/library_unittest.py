import unittest
from unittest.mock import patch

from libraries.library_app import app, Library


class TestAddBook(unittest.TestCase):  # Ran 4 tests in 0.009s
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    @patch.object(Library, 'add_book')
    def test_add_book(self, mock_add_book):
        mock_book_id = 123
        mock_add_book.return_value = mock_book_id
        
        response = self.client.post('/add_book', json={'title': 'Test Book'})

        mock_add_book.assert_called_once_with('Test Book')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": f"Book 'Test Book' added to the library with ID {mock_book_id}"})

    @patch.object(Library, 'borrow_book')
    def test_borrow_book(self, mock_borrow_book):
        mock_borrow_book.return_value = 'Test Book'

        response = self.client.post('/borrow_book', json={'title': 'Test Book'})

        mock_borrow_book.assert_called_once_with('Test Book')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Book 'Test Book' borrowed"})

    @patch.object(Library, 'return_book')
    def test_return_book(self, mock_return_book):
        mock_return_book.return_value = 'Test Book'

        response = self.client.post('/return_book', json={'title': 'Test Book'})

        mock_return_book.assert_called_once_with('Test Book')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Book 'Test Book' returned"})

    @patch.object(Library, 'available_books')
    def test_available_books(self, mock_available_books):
        mock_available_books.return_value = ['Test Book 1', 'Test Book 2']

        response = self.client.get('/available_books')

        mock_available_books.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, ['Test Book 1', 'Test Book 2'])
