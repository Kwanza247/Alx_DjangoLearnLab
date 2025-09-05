from relationship_app.models import Author, Book, Library, Librarian
# List all books in a library

def get_books_in_library(library_name):
    return Library.objects.get(name=library_name).books.all()


# Query all books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)

# Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    return Library.objects.get(name=library_name).librarian

