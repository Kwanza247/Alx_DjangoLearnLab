from django.shortcuts import render, redirect
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView

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
    

# relationship_app/views.py

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import View

# Login
class UserLoginView(LoginView):
    template_name = 'relationship_app/login.html'

# Logout
class UserLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'

# Register
class UserRegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'relationship_app/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # after registration go to login
        return render(request, 'relationship_app/register.html', {'form': form})
