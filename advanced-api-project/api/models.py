from django.db import models

# Create your models here.
class Author(models.Model):
    """
    Author model represents a book author.
    Each Author can have multiple Books (One-to-Many).
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model represents a book.
    Each Book is linked to exactly one Author.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
