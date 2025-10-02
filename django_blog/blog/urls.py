# blog/urls.py
from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(next_page='blog:login'), name='logout'),
    path('profile/', views.profile_view, name='profile'),

     # posts CRUD
    path('post/', views.PostListView.as_view(), name='post-list'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
      #tagging and searching
    path('tags/<str:tag_name>/', views.PostsByTagView.as_view(), name='posts_by_tag'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
]
