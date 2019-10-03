from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import UserProfile


class UserRegister(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']

        user_check = User.objects.filter(username=username)
        if not user_check:
            new_user = User.objects.create_user(username=username, password=password)
            token, _ = Token.objects.get_or_create(user=new_user)
            return Response("User is created")
        else:
            return Response("We have already the same username")


class UserLogin(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        data = request.data
        username = data['username']
        password = data['password']
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password!'})
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid credentials!'})
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,
                         'user_id': user.id,
                         'username': user.username,
                         })


class UserLogout(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        if request.user:
            request.user.auth_token.delete()
        else:
            Response("Please login first")
        return Response("Successfully logged out")


class UserUpdate(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    lookup_field = 'id'

    def get_queryset(self, user_id):
        return User.objects.filter(id=user_id)


class UserDelete(RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    lookup_field = 'id'

    def get_queryset(self, user_id):
        return User.objects.filter(id=user_id)