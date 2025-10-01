Blog Post CRUD - django_blog

Overview:
Implements List, Detail, Create, Update, Delete for the Post model using Django Class-Based Views.

Files added/modified:
- blog/forms.py         -> PostForm (ModelForm for Post)
- blog/views.py         -> PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
- blog/urls.py          -> posts/ routes (list, new, detail, edit, delete)
- blog/templates/blog/posts/ -> post_list.html, post_detail.html, post_form.html, post_confirm_delete.html
- blog/admin.py         -> ensure Post registered

Permissions:
- Create: only authenticated users (LoginRequiredMixin)
- Update/Delete: only the post author (UserPassesTestMixin)
- List/Detail: public

How author is set:
- PostCreateView.form_valid() sets form.instance.author = request.user

Testing:
- Manual steps: visit /posts/, /posts/new/ (logged-in), /posts/<pk>/, /posts/<pk>/edit/, /posts/<pk>/delete/
