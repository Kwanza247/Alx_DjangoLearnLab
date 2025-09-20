from django.urls import path, include
from .views import BookListCreateAPIView
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

urlpatterns = [
    path("api/books/", BookList.as_view(), name="book_list_create"),
]


# Create a router and register BookViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),

    # Include router-generated URLs
    path('', include(router.urls)),
]
