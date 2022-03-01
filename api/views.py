from .models import Movie
from .serializer import *
from dataclasses import field
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import BrowsableAPIRenderer
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    DestroyAPIView,
    UpdateAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateDestroyAPIView
)

# Create your views here.
from django.views.generic import (
    DetailView, 
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView
)


class MovieDetailView(ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Movie
    serializer_class = MovieSerializerInsert
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.objects.filter(movie_id=self.kwargs['pk'])

class MovieView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    
    queryset = Movie.objects.all()
    serializer_class = MovieSerializerInsert

class MovieFetchallView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Movie
    serializer_class = ModelSelializerViewAll
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.objects.filter(movie_id=self.kwargs['pk'])








####################################  deprecated  ############################################



# @api_view(['GET'])
# def movieList_id(request, pk):
#     try:
#         lib = Movie.objects.get(movie_id=pk)
#         serializer = MovieSerializerView(lib)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     except:
#         return Response([], status=status.HTTP_404_NOT_FOUND)

# @api_view(['GET'])
# def movieList(request):
#     lib = Movie.objects.all()
#     serializer = MovieSerializerView(lib, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def moviePost(request):
#     serializer = MovieSerializerInsert(data=request.data)
#     try:
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     except:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['PUT'])
# def moviePut(request, pk):
#     try:
#         lib = Movie.objects.get(movie_id=pk)
#         serializer = MovieSerializerInsert(lib, data=request.data)
#     except:
#         return Response([], status=status.HTTP_404_NOT_FOUND)
#     try:
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     except:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['DELETE'])
# def movieDelete(request, pk):
#     try:
#         lib = Movie.objects.get(movie_id=pk)
#     except:
#         return Response([], status=status.HTTP_404_NOT_FOUND)
#     try:
#         lib.delete()
#         return Response("DELETE", status=status.HTTP_200_OK)
#     except:
#         return Response("ERROR", status=status.HTTP_400_BAD_REQUEST)


