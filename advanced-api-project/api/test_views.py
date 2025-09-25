from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from api.models import Book, Author


class BookAPITests(APITestCase):

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username="testuser", password="password123")

        # Create an author
        self.author = Author.objects.create(name="Chinua Achebe")

        # Create a book
        self.book = Book.objects.create(title="Things Fall Apart", author=self.author, publication_year=1958)

        # Authentication helper
        self.client.login(username="testuser", password="password123")

    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Things Fall Apart", str(response.data))

    def test_retrieve_book(self):
        url = reverse("book-detail", kwargs={"pk": self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Things Fall Apart")
    
    def test_create_book(self):
        url = reverse("book-create")
        data = {
            "title": "Arrow of God",
            "publication_year": 1964,   # ✅ required field added
            "author": self.author.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.latest("id").title, "Arrow of God") 
    
    def test_update_book(self):
        self.client.force_authenticate(user=self.user)  # authenticate test client

        url = reverse("book-update", kwargs={"pk": self.book.id})
        data = {
            "title": "Things Fall Apart (Updated)",
            "publication_year": 1959,
            "author": self.author.id
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Things Fall Apart (Updated)")
        self.assertEqual(self.book.publication_year, 1959)

    
    def test_delete_book(self):
        url = reverse("book-delete", kwargs={"pk": self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_permission_for_unauthenticated_users(self):
        url = reverse("book-create")
        self.client.logout()
        data = {
            "title": "No Longer at Ease",
            "publication_year": 1960,
            "author": self.author.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
