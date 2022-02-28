from django.db.models import (
    Model, 
    IntegerField, 
    UUIDField, 
    BooleanField, 
    BigAutoField, 
    TextField, 
    CharField,
    JSONField,
    FloatField,
    DateTimeField,
    SlugField,
)

from django.db.models.signals import pre_save
from .utils import *
from datetime import datetime as dt
from django.db import models
from random import randint
import uuid

# Create your models here.

class Movie(Model):
    uuid = UUIDField(default=uuid.uuid4, unique=True, null=False)
    movie_id = IntegerField(unique=True)
    adult = BooleanField(default=False)
    backdrop_path = CharField(max_length=255, default="")
    genre_ids = JSONField(null=True)
    original_language = CharField(max_length=255, default="")
    original_title = CharField(max_length=255)
    overview = TextField(blank=True)
    poster_path = CharField(max_length=255, default="")
    release_date = CharField(max_length=255, default="")
    title = CharField(max_length=255)
    video = BooleanField(default=False)
    vote_average = FloatField()
    vote_count = IntegerField()
    popularity = FloatField()
    media_type = CharField(max_length=255, default="movie")
    updated_at = DateTimeField(auto_now_add=True)
    created_at = DateTimeField(auto_now_add=True)
    
    
    backdrop_b64 = TextField(null=True, blank=True)
    poster_b64 = TextField(null=True, blank=True)
    slug = SlugField(null=True, unique=True, blank=True)
    title_norm = CharField(max_length=255, null=True, blank=True)
    recommended = JSONField(null=True)
    
    
    budget = IntegerField(null=True)
    homepage = CharField(max_length=255, null=True, blank=True)
    imdb_id = CharField(max_length=255, null=True, blank=True)
    production_companies = JSONField(null=True)
    production_countries = JSONField(null=True)
    revenue = IntegerField(null=True)
    runtime = IntegerField(null=True)
    spoken_languages = JSONField(null=True)
    status = CharField(max_length=255, null=True, blank=True)
    tagline = CharField(max_length=255, null=True, blank=True)
    
    # def __init__(self, *args, **kwargs) -> None:
    #     self.setAllWithEval(kwargs)
    #     super().__init__(*args,**kwargs)

    # def setAllWithEval(self, kwargs):
    #     for key in list(kwargs.keys()):
    #         if key in ('id'):
    #             kwargs['movie_id'] = kwargs[key]
    #             del kwargs[key]
    #         if key not in ('uuid', 'created_at', 'updated_at'):
    #             setattr(self, key, kwargs[key])
    
    @property
    def name(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.backdrop_b64 :
            backdrop_inst_b64(self, save=False)
        if not self.poster_b64 :
            poster_inst_b64(self, save=False)
        if not self.slug :
            slugify_inst_title(self, save=False)
        if not self.recommended:
            recommended_item(self, save=False)
        conds = [
            self.budget, self.homepage, 
            self.imdb_id, self.production_companies, 
            self.production_countries, self.revenue, 
            self.runtime, self.spoken_languages,
            self.status, self.tagline
        ]
        if not all(conds):
            add_infos(self, save=False)
        super().save(*args, **kwargs)

def slug_pre_save(sender, instance, *args, **kwargs):
    if not instance.backdrop_b64:
        backdrop_inst_b64(instance, save=False)
    if not instance.poster_b64:
        poster_inst_b64(instance, save=False)
    if not instance.slug:
        slugify_inst_title(instance, save=False)
    if not instance.recommended:
        recommended_item(instance, save=False)
    conds = [
        instance.budget, instance.homepage, 
        instance.imdb_id, instance.production_companies, 
        instance.production_countries, instance.revenue, 
        instance.runtime, instance.spoken_languages,
        instance.status, instance.tagline
    ]
    if not all(conds): 
        add_infos(instance, save=False)

pre_save.connect(slug_pre_save, sender=Movie)