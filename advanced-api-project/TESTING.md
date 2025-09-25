Overview

This document explains the testing strategy, test cases, and guidelines used to verify the functionality, security, and data integrity of the Book API built with Django REST Framework (DRF).

All tests are located in:

/api/test_views.py

Testing Strategy

CRUD Operations

Ensure that books can be created, listed, retrieved, updated, and deleted via API endpoints.

Permissions & Authentication

Verify that only authenticated users can create, update, or delete books.

Confirm that unauthenticated users have read-only access.

Response Data Integrity

Ensure response payloads contain correct fields (id, title, author, publication_year).

Validate correct data is returned after create, update, and delete actions.

Status Codes

Verify correct HTTP response codes (200 OK, 201 Created, 204 No Content, 403 Forbidden).

Test Cases Implemented
1. List Books

Endpoint: GET /books/

Expected: 200 OK and a list of all available books.

2. Retrieve Book

Endpoint: GET /books/<id>/

Expected: 200 OK and details of the requested book.

3. Create Book (Authenticated)

Endpoint: POST /books/create/

Expected: 201 Created and new book is added to the database.

4. Update Book (Authenticated)

Endpoint: PUT /books/update/<id>/

Expected: 200 OK, and updated details are saved.

5. Delete Book (Authenticated)

Endpoint: DELETE /books/delete/<id>/

Expected: 204 No Content and book is removed.

6. Permission Check (Unauthenticated)

Endpoint: POST /books/create/

Expected: 403 Forbidden for unauthenticated requests.

How to Run Tests

Navigate to the project root directory (advanced-api-project).

Run the following command:

python manage.py test api

Sample Test Output
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......
----------------------------------------------------------------------
Ran 6 tests in 10.201s

OK
Destroying test database for alias 'default'...


✅ All tests passed successfully.