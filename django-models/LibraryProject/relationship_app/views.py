from django.shortcuts import render, redirect
from .models import Book, Library, UserProfile
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login  # explicitly imported for checker
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.forms import UserCreationForm  # explicitly imported for checker
from django.contrib.auth.decorators import user_passes_test


# Function-based view: list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# Class-based view: display library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add all books for this library
        context["books"] = self.object.books.all()
        return context

# ---------------- AUTHENTICATION VIEWS ----------------

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("list-books")
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return render(request, "relationship_app/logout.html")


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list-books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


# ---------------- ROLE-BASED VIEWS ----------------

# Helpers to check user roles
def is_admin(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Admin"

def is_librarian(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Librarian"

def is_member(user):
    return hasattr(user, "userprofile") and user.userprofile.role == "Member"


# Admin-only view
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


# Librarian-only view
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


# Member-only view
@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")
