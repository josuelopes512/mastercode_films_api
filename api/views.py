from dataclasses import field
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view



# Create your views here.
from .serializer import *
from .models import Movie
from rest_framework.viewsets import ModelViewSet
from django.views.generic import (
    DetailView, 
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView
)

@api_view(['GET'])
def movieList_id(request, pk):
    try:
        lib = Movie.objects.get(movie_id=pk)
        serializer = MovieSerializerView(lib)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except:
        return Response([], status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def movieList(request):
    lib = Movie.objects.all()
    serializer = MovieSerializerView(lib, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def moviePost(request):
    serializer = MovieSerializerInsert(data=request.data)
    try:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def moviePut(request, pk):
    try:
        lib = Movie.objects.get(movie_id=pk)
        serializer = MovieSerializerInsert(lib, data=request.data)
    except:
        return Response([], status=status.HTTP_404_NOT_FOUND)
    try:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def movieDelete(request, pk):
    try:
        lib = Movie.objects.get(movie_id=pk)
    except:
        return Response([], status=status.HTTP_404_NOT_FOUND)
    try:
        lib.delete()
        return Response("DELETE", status=status.HTTP_200_OK)
    except:
        return Response("ERROR", status=status.HTTP_400_BAD_REQUEST)



class MovieView(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializerInsert

class MovieDetailView(DetailView):
    model = Movie
    
class MovieListView(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieSetView(ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

class MovieCreateView(CreateView):
    model = Movie
    fields = [
        'movie_id', 
        'backdrop_path', 
        'genre_ids',
        'original_language',
        'original_title',
        'overview',
        'poster_path',
        'release_date',
        'title',
        'vote_average',
        'vote_count',
        'popularity',
    ]

class MovieUpdateView(UpdateView):
    model = Movie
    fields = [
        'movie_id', 
        'backdrop_path', 
        'genre_ids',
        'original_language',
        'original_title',
        'overview',
        'poster_path',
        'release_date',
        'title',
        'vote_average',
        'vote_count',
        'popularity',
    ]

class MovieDeleteView(DeleteView):
    model = Movie
    success_url = '/'


