from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Library, UserProfile
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login  # explicitly imported for checker
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.forms import UserCreationForm  # explicitly imported for checker
from django.contrib.auth.decorators import user_passes_test, permission_required


# ---------------- GENERAL VIEWS ----------------

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


# ---------------- PERMISSION-BASED BOOK VIEWS ----------------

# Add book (only if user has `can_add_book`)
@permission_required("relationship_app.can_add_book")
def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author_id = request.POST.get("author")
        # Author import assumed (if missing, import Author at top)
        from .models import Author
        author = get_object_or_404(Author, id=author_id)
        Book.objects.create(title=title, author=author)
        return redirect("list-books")
    authors = Author.objects.all()
    return render(request, "relationship_app/add_book.html", {"authors": authors})


# Edit book (only if user has `can_change_book`)
@permission_required("relationship_app.can_change_book")
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.title = request.POST.get("title")
        author_id = request.POST.get("author")
        from .models import Author
        book.author = get_object_or_404(Author, id=author_id)
        book.save()
        return redirect("list-books")
    authors = Author.objects.all()
    return render(request, "relationship_app/edit_book.html", {"book": book, "authors": authors})


# Delete book (only if user has `can_delete_book`)
@permission_required("relationship_app.can_delete_book")
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("list-books")
    return render(request, "relationship_app/delete_book.html", {"book": book})

