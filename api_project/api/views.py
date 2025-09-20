"""
Authentication & Permissions:
- TokenAuthentication enabled in settings.py
- Token retrieval: POST /api-token-auth/ {username, password}
- Permissions:
    * IsAuthenticated: required for all endpoints
    * IsAdminUser: required for destructive actions (delete)
"""

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Book
from .serializers import BookSerializer

class BookListCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # 🔒 must be logged in

class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Example: only admins can DELETE
    def get_permissions(self):
        if self.action in ['destroy']:  
            return [IsAdminUser()]
        return [IsAuthenticated()]

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

