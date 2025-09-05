from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic import DetailView

# Create your views here.

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