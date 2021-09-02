from django.db import models
from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import viewsets

from .serializers import RoomListSerializer, BookingListSerializer
from .models import Room, Booking

from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib import auth
import jwt

# Create your views here.

class RoomList(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomListSerializer



class BookingList(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingListSerializer
    

class RegisterView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user:
            # auth_token = jwt.encode({'username': user.username}, settings.JWT_SECRET_KEY, algorithm="HS256") ////   something Wrong Here!!!!!!!!!!!!
            auth_token = jwt.encode({'email': user.email, 'username':user.username}, 'MySecretKey', algorithm='HS256')

            serializer = RegisterSerializer(user)

            data = {'user': serializer.data, 'token': auth_token}

            return Response(data, status=status.HTTP_200_OK)

            # SEND RES
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)