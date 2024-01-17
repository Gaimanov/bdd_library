import os
import sqlite3
from functools import wraps


def connection_helper(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        cursor = self.conn.cursor()
        try:
            return func(self, *args, cursor=cursor, **kwargs)
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []
        finally:
            cursor.close()
    return wrapper


class Library:
    def __init__(self, db_path=os.path.join(os.path.dirname(__file__), 'library.db')):
        self.conn = sqlite3.connect(db_path)
        self.init_db()

    def init_db(self):
        """ Initialize the database and tables """
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                borrowed BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        self.conn.commit()

    @connection_helper
    def add_book(self, title, cursor=None):
        cursor.execute('INSERT INTO books (title) VALUES (?)', (title,))
        self.conn.commit()
        return cursor.lastrowid

    @connection_helper
    def borrow_book(self, title, cursor=None):
        cursor.execute('''
            UPDATE books SET borrowed = 1 WHERE title = ? AND NOT borrowed
        ''', (title,))
        if cursor.rowcount > 0:
            self.conn.commit()
            return title
        return None

    @connection_helper
    def return_book(self, title, cursor=None):
        cursor.execute('''
            UPDATE books SET borrowed = 0 WHERE title = ?
        ''', (title,))
        if cursor.rowcount > 0:
            self.conn.commit()
            return title
        return None

    @connection_helper
    def is_book_available(self, title, cursor=None):
        cursor.execute('''
            SELECT * FROM books WHERE title = ? AND NOT borrowed
        ''', (title,))
        return cursor.fetchone() is not None

    @connection_helper
    def available_books(self, cursor=None):
        cursor.execute("SELECT title FROM books WHERE borrowed = False")
        books = cursor.fetchall()
        return [book[0] for book in books]

    @connection_helper
    def borrowed_books(self, cursor=None):
        cursor.execute("SELECT title FROM books WHERE borrowed = True")
        books = cursor.fetchall()
        return [book[0] for book in books]
