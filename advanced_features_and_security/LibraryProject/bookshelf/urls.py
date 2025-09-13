from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.book_list, name="book_list"),
    path("books/search/", views.search_books, name="search_books"),
    path("example-form/", views.example_form_view, name="example_form"),  # ✅ new
]
