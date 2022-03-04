from pprint import pprint
from .serializer import MovieSerializerInsert
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from threading import Thread, active_count
from .models import Movie
from pathlib import Path
from random import choice
from time import sleep

import os, sys, environ, threading, traceback, requests as req

sys.setrecursionlimit(10000)

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

movies_ids_sim = []

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
    sleep(choice(list(range(5, 11))))
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
        for i in list(dta.keys()):
            if not dta[i]:
                dta.pop(i)
        if not data:
            ddb = Movie(**dta)
            ddb.save()
    except Exception as e:
        logger(f"THREADS: {active_count()} TRACEBACK: {traceback.format_exc()}, {e}, FUNCTION: (save_banco), DATA: {dta}", movie_id=dta['movie_id'])

def add_similar(movie_id):
    try:
        threads_list = []
        recomendados = req.get(f"{URL_DB}/movie/{movie_id}/similar?api_key={API_KEY}&language=pt-BR&page=1")
        filmes_json = recomendados.json()
        if not (recomendados.status_code == 200):
            raise Exception
        if 'status_message' in filmes_json and 'success' in filmes_json and 'status_message' in filmes_json:
            raise Exception
        filmes_json_res = filmes_json['results']
        for i, mov in enumerate(filmes_json_res):
            data = Movie.objects.filter(movie_id=mov['id'])
            if not data:
                # threaded(save_banco, mov)
                print(f"THREADS: {active_count()} recomendados INDICE: {i} MOVIEID: {mov['id']}")
                th = Thread(target=save_banco, args=(mov,))
                # th.start()
                threads_list.append(th)
                if mov['id'] not in movies_ids_sim:
                    movies_ids_sim.append(mov['id'])
        for i in threads_list:
            while active_count()>100 :
                sleep(20)
            i.start()
            while i.is_alive():
                sleep(choice(list(range(5, 11))))
            sleep(choice(list(range(5, 11))))
    except Exception as e:
        logger(f"TRACEBACK: {traceback.format_exc()}, {e}, FUNCTION: (add_similar), DATA: {filmes_json}", movie_id=movie_id)


def add_movie_id(movie_id):
    try:
        movie_i_req = req.get(f"{URL_DB}/movie/{movie_id}?api_key={API_KEY}&language=pt-BR")
        movie_i = movie_i_req.json()
        
        if not (movie_i_req.status_code == 200):
            raise Exception
        if 'status_message' in movie_i or 'success' in movie_i or 'status_message' in movie_i:
            raise Exception
        # threaded(save_banco, movie_i)
        save_banco(movie_i)
    except Exception as e:
        logger(f"TRACEBACK: {traceback.format_exc()}, {e}, FUNCTION: (add_movie_id), DATA: {movie_i}", movie_id=movie_id)

def trending_movie(ini=1, fim=100):
    print("Downloading databases .........")
    for i in range(ini, fim+1):
        try:
            pag = req.get(f'{URL_DB}/trending/movie/week?api_key={API_KEY}&language=pt-BR&page={i}&include_adult=true')
            json_pag = pag.json()
            data = json_pag['results']
            for ind, dta in enumerate(data):
                try:
                    data = Movie.objects.filter(movie_id=dta['id'])
                    if not data:
                        # threaded(add_movie_id, dta['id'])
                        print(f"ENUM: {threading.active_count()}, trending_movie INDICE: {ind} MOVIEID: {dta['id']}")
                        th = Thread(target=add_movie_id, args=(dta['id'],))
                        th.start()
                        th2 = Thread(target=add_similar, args=(dta['id'],))
                        th2.start()
                        while active_count()>100 :
                            sleep(5)
                        # while th.is_alive() and th2.is_alive():
                        #     sleep(5)
                        #     continue
                        # th.join()
                except Exception as e:
                    logger(f"{e}, FUNCTION: (trending_movie-2), ind: {ind}, DATA: {dta}")
            # print("Processing databases .........")
        except Exception as e:
            logger(f"{e}, FUNCTION: (trending_movie), ind: {i}")
            continue
    # print("OK")
    print(len(movies_ids_sim))


def threaded(target, args):
    while active_count()>100 :
        sleep(5)
    th = Thread(target=target, args=(args,))
    th.start()
    th.join()

def logger(e, movie_id=0):
    with open("errors.log", "a", encoding="utf-8") as f:
        f.write(f"ERROR: {e}, movie_id: {movie_id}\n")