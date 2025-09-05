from django.urls import path
from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    # Function-based view for listing all books
    path("books/", list_books, name="list-books"),

    # Class-based view for library details
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library-detail"),
]


urlpatterns = [
    # Function-based view for listing all books
    path("books/", views.list_books, name="list-books"),

    # Class-based view for library details
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library-detail"),
]
