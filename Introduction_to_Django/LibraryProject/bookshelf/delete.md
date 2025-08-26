from bookshelf.models import Book
book = Book.objects.get(id=1)
book.delete()
print(book.__dict__)

''' Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "C:\Users\Dell\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages\django\db\models\manager.py", line 87, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\Dell\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages\django\db\models\query.py", line 633, in get
    raise self.model.DoesNotExist(
        "%s matching query does not exist." % self.model._meta.object_name
    )`
'''