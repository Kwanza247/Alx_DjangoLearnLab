## API Endpoints

- `GET /api/books/` → List all books (public)
- `POST /api/books/` → Create new book (authenticated only)
- `GET /api/books/<id>/` → Retrieve a book by ID (public)
- `PUT /api/books/<id>/` → Update a book (authenticated only)
- `DELETE /api/books/<id>/` → Delete a book (authenticated only)

### Permissions
- Unauthenticated users → read-only
- Authenticated users → full CRUD access


### Filtering, Searching & Ordering
- Filter: `/books/?publication_year=1958`
- Search: `/books/?search=Arrow`
- Order: `/books/?ordering=-publication_year`
