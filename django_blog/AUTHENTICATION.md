AUTHENTICATION SYSTEM - django_blog

Overview:
This implements registration, login, logout, and profile management.

Files added/modified:
- blog/forms.py         -> CustomUserCreationForm, ProfileForm
- blog/models.py        -> Profile (OneToOne with User) and signals
- blog/views.py         -> register_view, class-based LoginView & LogoutView, profile_view
- blog/urls.py          -> register/, login/, logout/, profile/
- blog/templates/blog/  -> register.html, login.html, logout.html, profile.html
- blog/admin.py         -> register Post and Profile in admin
- django_blog/urls.py   -> include('blog.urls')
- django_blog/settings.py -> MEDIA_URL, MEDIA_ROOT, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL (ensure present)

Setup:
1. If you want avatars: install Pillow: `pip install Pillow`
2. Run migrations:
   python manage.py makemigrations
   python manage.py migrate
3. Create a superuser (optional):
   python manage.py createsuperuser
4. Start server:
   python manage.py runserver

Testing:
- Register at /register/
- Login at /login/
- Logout at /logout/
- Edit profile at /profile/

Security:
- CSRF protection enabled in all templates (templates include {% csrf_token %}).
- Passwords use Django's secure hashing algorithm.
- Profile editing requires authentication.

Notes:
- Avatar files are stored under MEDIA_ROOT/avatars/ if uploaded.
- If you don't want images, you may ignore avatar field; no harm leaving it blank.
