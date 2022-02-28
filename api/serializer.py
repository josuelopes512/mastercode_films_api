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
        # (
        #     'movie_id', 'backdrop_path', 
        #     'genre_ids', 'original_language',
        #     'original_title', 'overview',
        #     'poster_path', 'release_date',
        #     'title', 'vote_average',
        #     'vote_count', 'popularity',
        #     'media_type', "budget", 
        #     "homepage", "imdb_id", 
        #     "production_companies", "production_countries", 
        #     "revenue", "runtime", "spoken_languages",
        #     "status", "tagline"
        # )


class MovieSerializerView(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'movie_id',
            'uuid',
            'adult', 
            'backdrop_path',
            'backdrop_b64', 
            'genre_ids',
            'original_language',
            'original_title',
            'overview',
            'poster_path',
            'poster_b64',
            'release_date',
            'title',
            'slug',
            'title_norm',
            'video',
            'vote_average',
            'vote_count',
            'popularity',
            'recommended',
            'media_type',
            'created_at',
            'updated_at'
        )