from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    RetrieveTokenView,
    FollowUserView,
    UnfollowUserView,
    FollowingListView,
)

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/', RetrieveTokenView.as_view(), name='retrieve-token'),

    # Follow System
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('following/', FollowingListView.as_view(), name='following-list'),
]
