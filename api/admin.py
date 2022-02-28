from django.contrib import admin

# Register your models here.

from .models import Movie

class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie_id', 'title', 'slug']
    prepopulated_fields = {
        "slug": ("title",)
    }

admin.site.register(Movie, MovieAdmin)