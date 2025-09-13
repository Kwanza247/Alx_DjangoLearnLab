from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm   # ✅ import form

# Create your views here.

# Example form view with CSRF protection
def example_form_view(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Handle the form securely here
            return HttpResponse("Form submitted successfully!")
    else:
        form = ExampleForm()
    return render(request, "bookshelf/form_example.html", {"form": form})

# ✅ Search books safely
def search_books(request):
    query = request.GET.get("q", "")
    books = Book.objects.filter(title__icontains=query)  # ORM auto sanitizes input
    return render(request, "bookshelf/book_list.html", {"books": books})

@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})

@permission_required("bookshelf.can_create", raise_exception=True)
def add_book(request):
    return HttpResponse("Only users with can_create can see this.")

@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"Editing {book.title}")

@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"Deleting {book.title}")
