book = Book.objects.get(id=1)

book.title = "Nineteen Eighty-Four"
book.save
print(book.title)
# Nineteen Eighty-Four
print(book.__dict__)
{'_state': <django.db.models.base.ModelState object at 0x000002BD92542710>, 'id': 1, 'title': 'Nineteen Eighty-Four', 'author': 'ibrahim', 'publication_year': 1990}