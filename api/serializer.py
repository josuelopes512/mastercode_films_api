from dataclasses import field
from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('movie_id', 'title')


class MovieSerializerInsert(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            "movie_id", "adult", "backdrop_path",
            "genre_ids", "original_language", "original_title",
            "overview", "poster_path", "release_date",
            "title", "video", "vote_average",
            "vote_count", "popularity", "media_type"
        ]


class MovieSerializerView(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'movie_id','uuid','adult', 'backdrop_path','backdrop_b64', 'genre_ids',
            'original_language','original_title','overview','poster_path','poster_b64',
            'release_date','title','slug','title_norm','video','vote_average','vote_count',
            'popularity','recommended','media_type','created_at','updated_at'
        )

class ModelSelializerViewAll(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'uuid','movie_id','adult','backdrop_path','genre_ids','original_language',
            'original_title','overview','poster_path','release_date','title','video',
            'vote_average','vote_count','popularity','media_type','updated_at','created_at',
            'backdrop_b64','poster_b64','slug','title_norm','recommended','budget','homepage',
            'imdb_id','production_companies','production_countries','revenue','runtime',
            'spoken_languages','status', 'tagline'
        )