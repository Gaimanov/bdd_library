from behave import given, when, then


@given('the library_app has a copy of "{book}"')
def step_impl(context, book):
    with context.library.test_client() as client:
        response = client.post('/add_book', json={'title': book})
        assert response.status_code == 201
        context.response = response


@when('I borrow "{book}"')
def step_impl(context, book):
    with context.library.test_client() as client:
        response = client.post('/borrow_book', json={'title': book})
        assert response.status_code == 200
        context.borrow_response = response


@then('I should have "{book}" in my borrowed list')
def step_impl(context, book):
    with context.library.test_client() as client:
        response = client.get('/borrowed_books')
        borrowed_books = response.json
        print(f"Books: {borrowed_books}")
        assert book in borrowed_books


@given('I have "{book_title}" borrowed from the library_app')
def step_impl(context, book_title):
    with context.library.test_client() as client:
        client.post('/borrow_book', json={'title': book_title})
        response = client.get(f'/is_book_available?title={book_title}')
        is_available = response.json.get('is_available')
        assert not is_available, f"{book_title} should not be available after borrowing"


@when('I return "{book_title}"')
def step_impl(context, book_title):
    with context.library.test_client() as client:
        _ = client.post('/return_book', json={'title': book_title})


@then('"{book_title}" should be available in the library_app again')
def step_impl(context, book_title):
    with context.library.test_client() as client:
        response = client.get(f'/is_book_available?title={book_title}')
        is_available = response.json.get('is_available')
        assert is_available, f"{book_title} should be available after returning"

