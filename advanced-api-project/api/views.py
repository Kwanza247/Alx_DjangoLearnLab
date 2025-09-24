from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


# List all books or create a new one
class BookListCreateView(generics.ListCreateAPIView):
    """
    GET: Return a list of all books
    POST: Create a new book (authenticated users only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Permissions: anyone can read, only authenticated can create
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


# Retrieve, update, or delete a book by ID
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a single book
    PUT/PATCH: Update an existing book (authenticated users only)
    DELETE: Remove a book (authenticated users only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Permissions: anyone can read, only authenticated can update/delete
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
