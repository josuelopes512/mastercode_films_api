from pprint import pprint
from .serializer import MovieSerializerInsert
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from threading import Thread, active_count
from .models import Movie
from pathlib import Path
from time import sleep

import os, environ, requests as req

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

URL_DB = 'https://api.themoviedb.org/3'
API_KEY= env('API_KEY')

session = req.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)


def get_token():
    ip_addr ="http://localhost:8000"
    data_inf = {
        "username": "admin",
        "password": "admin"
    }
    token = session.post(f"{ip_addr}/token/", json=data_inf).json()
    return {
        "accept": "application/json",
        "Authorization": f"Bearer {token['access']}",
    }

def save_banco(dta):
    try:
        if 'id' in dta:
            dta['movie_id'] = dta['id']
            dta.pop('id')
        if 'genres' in dta:
            dta['genre_ids'] = [i['id'] for i in dta['genres']]
            dta.pop('genres')
        for i in list(dta.keys()):
            if not i in MovieSerializerInsert.Meta.fields:
                dta.pop(i)
        data = Movie.objects.filter(movie_id=dta['movie_id'])
        if not data:
            ddb = Movie(**dta)
            ddb.save()
    except Exception as e:
        with open("errors.log", "a") as f:
            f.write(f"ERROR: {e}, movie_id: {dta['movie_id']}\n")

def add_movie_id(movie_id):
    try:
        movie_i_req = req.get(f"{URL_DB}/movie/{movie_id}?api_key={API_KEY}&language=pt-BR")
        movie_i = movie_i_req.json()
        threaded(save_banco, movie_i)
    except Exception as e:
        print(f"ERROR: {e}")
    
    try:
        recomendados = req.get(f"{URL_DB}/movie/{movie_id}/similar?api_key={API_KEY}&language=pt-BR&page=1")
        filmes_json = recomendados.json()
        filmes_json = filmes_json['results']
        for mov in filmes_json:
            threaded(save_banco, mov)
    except Exception as e:
        print(f"ERROR: {e}")

def trending_movie(ini=1, fim=100):
    print("Downloading databases .........")
    for i in range(ini, fim+1):
        try:
            pag = req.get(f'{URL_DB}/trending/movie/week?api_key={API_KEY}&language=pt-BR&page={i}&include_adult=true')
            json_pag = pag.json()
            data = json_pag['results']
            for dta in data:
                data = Movie.objects.filter(movie_id=dta['id'])
                if not data:
                    threaded(add_movie_id, dta['id'])
            print("Processing databases .........")
        except:
            continue
    print("OK")


def threaded(target, args):
    while active_count()>150 :
        sleep(0.01)
    th = Thread(target=target, args=(args,))
    th.start()
    th.join()