from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer
)
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_class = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

User = get_user_model()

# -------------------- AUTHENTICATION --------------------

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # fixed typo

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
            "token": token.key,
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)


class RetrieveTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token, _ = Token.objects.get_or_create(user=request.user)
        return Response({
            "token": token.key,
            "user": UserSerializer(request.user).data
        })


# -------------------- FOLLOW / UNFOLLOW --------------------

class FollowUserView(APIView):
    """
    Allows authenticated users to follow another user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response({"detail": "You cannot follow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            target_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."},
                            status=status.HTTP_404_NOT_FOUND)

        request.user.following.add(target_user)
        return Response(
            {"detail": f"You are now following {target_user.username}."},
            status=status.HTTP_200_OK
        )


class UnfollowUserView(APIView):
    """
    Allows authenticated users to unfollow another user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response({"detail": "You cannot unfollow yourself."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            target_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."},
                            status=status.HTTP_404_NOT_FOUND)

        request.user.following.remove(target_user)
        return Response(
            {"detail": f"You have unfollowed {target_user.username}."},
            status=status.HTTP_200_OK
        )


class FollowingListView(APIView):
    """
    Returns the list of users that the current user is following.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        following_users = request.user.following.all()
        data = [{"id": user.id, "username": user.username, "email": user.email}
                for user in following_users]
        return Response(data, status=status.HTTP_200_OK)

        token, _= Token.objects.get_or_create(user=user)

        return Response ({
            "user": UserSerializer(user).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)
    
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serialiazer = self.get_serializer (data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serialiazer.validated_data['user']
        token, _= Token.objects.get_or_create(user=user)

        return Response ({
            "token": token.key,
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class RetrieveTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token, _= Token.objects.get_or_create(user=request.user)
        return Response({
            "token": token.key,
            "user": UserSerializer(request.user).data
        })