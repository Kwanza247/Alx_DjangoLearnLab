from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# New ViewSet for CRUD
class BookViewSet(viewsets.ModelViewSet):  # ✅ ModelViewSet handles CRUD
    queryset = Book.objects.all()
    serializer_class = BookSerializer
