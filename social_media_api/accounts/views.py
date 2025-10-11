from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

# ✅ Import Notification model safely
try:
    from notifications.models import Notification
except Exception:
    Notification = None

CustomUser = get_user_model()


# -------------------- AUTHENTICATION --------------------

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

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
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key,
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)


class RetrieveTokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        token, _ = Token.objects.get_or_create(user=request.user)
        return Response({
            "token": token.key,
            "user": UserSerializer(request.user).data
        }, status=status.HTTP_200_OK)


# -------------------- FOLLOW / UNFOLLOW --------------------

class FollowUserView(APIView):
    """Allows authenticated users to follow another user."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response({"detail": "You cannot follow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)

        user_to_follow = get_object_or_404(CustomUser.objects.all(), pk=user_id)
        request.user.following.add(user_to_follow)

        # ✅ Create a notification for the user being followed
        if Notification and user_to_follow != request.user:
            Notification.objects.create(
                recipient=user_to_follow,
                actor=request.user,
                verb='started following you'
            )

        return Response(
            {"detail": f"You are now following {user_to_follow.username}."},
            status=status.HTTP_200_OK
        )


class UnfollowUserView(APIView):
    """Allows authenticated users to unfollow another user."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response({"detail": "You cannot unfollow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)

        user_to_unfollow = get_object_or_404(CustomUser.objects.all(), pk=user_id)
        request.user.following.remove(user_to_unfollow)

        return Response(
            {"detail": f"You have unfollowed {user_to_unfollow.username}."},
            status=status.HTTP_200_OK
        )


class FollowingListView(APIView):
    """Returns the list of users that the current user is following."""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        following_users = request.user.following.all()
        data = [
            {"id": user.id, "username": user.username, "email": user.email}
            for user in following_users
        ]
        return Response(data, status=status.HTTP_200_OK)
