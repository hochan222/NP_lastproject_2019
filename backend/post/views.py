from django.shortcuts import render
from rest_framework import generics

from .models import Post, Bachelor_data, IoT_data
from .serializers import PostSerializer, BachelorSerializer, IoTSerializer


class ListPost(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class DetailPost(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ListBachelorData(generics.ListCreateAPIView):
    queryset = Bachelor_data.objects.all()
    serializer_class = BachelorSerializer

class IoTPost(generics.ListCreateAPIView):
    queryset = IoT_data.objects.all()
    serializer_class = IoTSerializer