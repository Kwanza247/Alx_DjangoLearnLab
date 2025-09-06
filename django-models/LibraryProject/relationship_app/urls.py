from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Book list and library detail
    path("books/", views.list_books, name="list-books"),
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library-detail"),

    # Authentication using Django’s built-in views
    path("login/", LoginView.as_view(template_name="relationship_app/login.html"), name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", views.register_view, name="register"),

    # Role-based access control URLs
    path("admin-view/", views.admin_view, name="admin-view"),
    path("librarian-view/", views.librarian_view, name="librarian-view"),
    path("member-view/", views.member_view, name="member-view"),

    # Permission-based book management URLs
    path("books/add/", views.add_book, name="add-book"),
    path("books/<int:pk>/edit/", views.edit_book, name="edit-book"),
    path("books/<int:pk>/delete/", views.delete_book, name="delete-book"),
]
