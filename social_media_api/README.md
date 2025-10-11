# 🌐 Social Media API — Follow System & Feed Feature

## 📘 Overview

This project extends the **Social Media API** built with **Django** and **Django REST Framework (DRF)**.  
It introduces **user following functionality** and a **personalized feed system** — allowing users to follow others and view posts made by the people they follow.  

Users can:
- Register, log in, and manage profiles
- Follow and unfollow other users
- View a feed of posts made by followed users
- Create, edit, and delete their own posts and comments

---

## ⚙️ Step 1: Project Setup

### 1. Install Dependencies
Make sure you have Django and DRF installed:

```bash
pip install django djangorestframework django-filter djangorestframework-simplejwt

In social_media_api/settings.py, ensure these apps are added:
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'accounts',
    'posts',
]

Step 2: User Model Update — Following System

In accounts/models.py:
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    def __str__(self):
        return self.username

Then update settings.py:
AUTH_USER_MODEL = 'accounts.User'
Run migrations:
python manage.py makemigrations
python manage.py migrate



🔐 Step 3: Authentication and Profile Management

accounts/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)
        request.user.following.add(target_user)
        return Response({"message": f"You are now following {target_user.username}"})

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)
        request.user.following.remove(target_user)
        return Response({"message": f"You unfollowed {target_user.username}"})
📡 Step 4: Feed Functionality

posts/views.py
from rest_framework import generics, permissions, filters, viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['post']
    search_fields = ['content']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        followed_users = user.following.all()
        return Post.objects.filter(author__in=followed_users).order_by('-created_at')


🔗 Step 5: URLs Configuration

accounts/urls.py
from django.urls import path
from .views import RegisterView, LoginView, ProfileView, FollowUserView, UnfollowUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow_user'),
]


posts/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
]

social_media_api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
]


social_media_api/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/', include('posts.urls')),
]


🧠 Testing the API

Use Postman or cURL to test:

Register
POST /api/accounts/register/
{
  "username": "ibrahim",
  "email": "ibrahim@example.com",
  "password": "mypassword"
}

Follow User
POST /api/accounts/follow/2/
Authorization: Token <your_token>


Feed
GET /api/feed/
Authorization: Token <your_token>


📁 Project Structure
social_media_api/
│
├── social_media_api/
│   ├── settings.py
│   ├── urls.py
│
├── accounts/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│
├── posts/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│
├── manage.py
└── README.md


✅ Deliverables

Updated user model with follow relationships

Follow/unfollow API endpoints

Feed endpoint displaying posts from followed users

CRUD operations for posts and comments

Comprehensive documentation (this README)