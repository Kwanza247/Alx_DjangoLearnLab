# blog/urls.py
from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='blog:login'), name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
