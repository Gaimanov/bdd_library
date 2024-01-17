from flask import Flask, jsonify, request
from libraries.lib import Library

app = Flask(__name__)
library = Library()


@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.json.get('title')
    book_id = library.add_book(title)
    return jsonify({"message": f"Book '{title}' added to the library with ID {book_id}"}), 201


@app.route('/borrow_book', methods=['POST'])
def borrow_book():
    title = request.json.get('title')
    book = library.borrow_book(title)
    if book:
        return jsonify({"message": f"Book '{title}' borrowed"}), 200
    else:
        return jsonify({"message": "Book not available"}), 404


@app.route('/return_book', methods=['POST'])
def return_book():
    title = request.json.get('title')
    book = library.return_book(title)
    if book:
        return jsonify({"message": f"Book '{title}' returned"}), 200
    else:
        return jsonify({"message": "Book not found in borrowed list"}), 404


@app.route('/available_books', methods=['GET'])
def available_books():
    return jsonify(library.available_books()), 200


@app.route('/borrowed_books', methods=['GET'])
def borrowed_books():
    return jsonify(library.borrowed_books()), 200


@app.route('/is_book_available', methods=['GET'])
def is_book_available():
    book_title = request.args.get('title')
    if book_title in library.available_books():
        return jsonify({'is_available': True}), 200
    else:
        return jsonify({'is_available': False}), 200


if __name__ == '__main__':
    app.run(debug=True)
