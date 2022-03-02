from django.utils.text import slugify 
from threading import Thread
from random import randint
from pathlib import Path

import environ, base64, requests as req


BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

API_KEY= env('API_KEY')
URL_DB = 'https://api.themoviedb.org/3'


def add_infos(instance, save=False, new_items=None):
    keys_d = [ 
        "budget", "homepage", "imdb_id", "production_companies", 
        "production_countries", "revenue", "runtime", "spoken_languages",
        "status", "tagline"
    ]
    if new_items:
        items = new_items
        for i in list(items.keys()):
            if not i in keys_d:
                items.pop(i)
    else:
        items = add_to_db(instance.movie_id)
    
    obj = instance.__class__
    
    qs_budget = obj.objects.filter(movie_id=instance.movie_id).exclude(budget=None)
    qs_homepage = obj.objects.filter(movie_id=instance.movie_id).exclude(homepage=None)
    qs_imdb_id = obj.objects.filter(movie_id=instance.movie_id).exclude(imdb_id=None)
    qs_production_companies = obj.objects.filter(movie_id=instance.movie_id).exclude(production_companies=None)
    qs_production_countries = obj.objects.filter(movie_id=instance.movie_id).exclude(production_countries=None)
    qs_revenue = obj.objects.filter(movie_id=instance.movie_id).exclude(revenue=None)
    qs_runtime = obj.objects.filter(movie_id=instance.movie_id).exclude(runtime=None)
    qs_spoken_languages = obj.objects.filter(movie_id=instance.movie_id).exclude(spoken_languages=None)
    qs_status = obj.objects.filter(movie_id=instance.movie_id).exclude(status=None)
    qs_tagline = obj.objects.filter(movie_id=instance.movie_id).exclude(tagline=None)
    
    in_conds = [
        qs_budget.exists(),
        qs_homepage.exists(),
        qs_imdb_id.exists(),
        qs_production_companies.exists(),
        qs_production_countries.exists(),
        qs_revenue.exists(),
        qs_runtime.exists(),
        qs_spoken_languages.exists(),
        qs_status.exists(),
        qs_tagline.exists()
    ]
    
    if any(in_conds):
        return add_infos(instance, save=save, new_items=items)
    instance.budget = items.get('budget', None)
    instance.imdb_id = items.get('imdb_id', None)
    instance.homepage = items.get('homepage', None)
    instance.production_companies = items.get('production_companies', None)
    instance.production_countries = items.get('production_countries', None)
    instance.revenue = items.get('revenue', None)
    instance.runtime = items.get('runtime', None)
    instance.spoken_languages = items.get('spoken_languages', None)
    instance.status = items.get('status', None)
    instance.tagline = items.get('tagline', None)
    
    if save:
        instance.save()
    return instance

def slugify_inst_title(instance, save=False, new_slug=None):
    if new_slug:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    obj = instance.__class__
    qs = obj.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        rand_int = randint(300_00, 500_00)
        slug = f"{slug}-{rand_int}"
        return slugify_inst_title(instance, save=save, new_slug=slug)
    instance.slug = slug
    instance.title_norm = slug.replace('-', ' ')
    if save:
        instance.save()
    return instance

def recommended_item(instance, save=False, new_rec=None):
    if new_rec:
        rec = new_rec
    else:
        rec = get_rec_similar(instance.movie_id)
    obj = instance.__class__
    qs = obj.objects.filter(recommended=rec).exclude(id=instance.id)
    if qs.exists():
        return recommended_item(instance, save=save, new_rec=rec)
    instance.recommended = rec
    if save:
        instance.save()
    return instance

def backdrop_inst_b64(instance, save=False, new_bd=None):
    if new_bd:
        bd = new_bd
    else:
        bd = jpg_to_base64(instance.backdrop_path)
    obj = instance.__class__
    qs = obj.objects.filter(backdrop_path=bd).exclude(id=instance.id)
    if qs.exists():
        rand_int = randint(300_00, 500_00)
        bd = f"{bd}-{rand_int}"
        return backdrop_inst_b64(instance, save=save, new_bd=bd)
    instance.backdrop_b64 = bd
    if save:
        instance.save()
    return instance

def poster_inst_b64(instance, save=False, new_bd=None):
    if new_bd:
        bd = new_bd
    else:
        bd = jpg_to_base64(instance.poster_path)
    obj = instance.__class__
    qs = obj.objects.filter(poster_path=bd).exclude(id=instance.id)
    if qs.exists():
        rand_int = randint(300_00, 500_00)
        bd = f"{bd}-{rand_int}"
        return poster_inst_b64(instance, save=save, new_bd=bd)
    instance.poster_b64 = bd
    if save:
        instance.save()
    return instance

def jpg_to_base64(link):
    if '.jpg' in link[-4:] and '/' in link[0]:
        try:
            img = req.get(f'https://image.tmdb.org/t/p/w154{link}')
            data = base64.b64encode(img.content).decode('utf-8')
            return data
        except:
            return ""

def get_rec_similar(movie_id):
    try:
        recomendados = req.get(f"{URL_DB}/movie/{movie_id}/similar?api_key={API_KEY}&language=pt-BR&page=1")
        filmes_json = recomendados.json()
        filmes_json = filmes_json['results']
        ids = [id['id'] for id in filmes_json]
        return ids
    except:
        return []

def add_to_db(movie_id):
    try:
        movie_i_req = req.get(f"{URL_DB}/movie/{movie_id}?api_key={API_KEY}&language=pt-BR")
        movie_i = movie_i_req.json()
        movie_i['genre_ids'] = [i['id'] for i in movie_i['genres']]
        movie_i['movie_id'] = movie_i['id']
        movie_i.pop('id')
        movie_i.pop('genres')
        return movie_i
    except Exception as e:
        print(f"CAIU AQUI ERROR: {e}")
        return {}

def get_add_trending(qtd=10):
    result = []
    for i in range(1, qtd):
        try:
            pag = req.get(f'{URL_DB}/trending/movie/week?api_key={API_KEY}&language=pt-BR&page={i}&include_adult=true')
            json_pag = pag.json()
            result += json_pag['results']
        except:
            continue
    return result

###########################################################################################################################

def get_token():
    data_inf = {
        "username": "admin",
        "password": "admin"
    }
    token = req.get(f"http://localhost:8000/token/", json=data_inf).json()
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {token['access']}",
    }

def save_banco(dta):
    try:
        dta['movie_id'] = dta['id']
        dta.pop('id')
        teste = req.get(f"http://localhost:8000/api/movie/{dta['movie_id']}")
        if teste.status_code != 200:
            teste = req.post("http://localhost:8000/api/movie/{dta['movie_id']}", json=dta, headers=get_token())
            if teste.status_code != 200:
                with open("error_400_z.json", "a") as f:
                    f.write(f"{dta['movie_id']} ------ {teste.json()}\n")
    except Exception as e:
        with open("errors_z.json", "a") as f:
            f.write(f"ERROR: {e}, movie_id: {dta['movie_id']}\n")

def add_movie_id(movie_id):
    try:
        movie_i_req = req.get(f"{URL_DB}/movie/{movie_id}?api_key={API_KEY}&language=pt-BR")
        movie_i = movie_i_req.json()
        Thread(target=save_banco, args=(movie_i,)).start()
    except:
        pass
    
    try:
        recomendados = req.get(f"{URL_DB}/movie/{movie_id}/similar?api_key={API_KEY}&language=pt-BR&page=1")
        filmes_json = recomendados.json()
        filmes_json = filmes_json['results']
        for mov in filmes_json:
            Thread(target=save_banco, args=(mov,)).start()
    except:
        pass

def trending_movie(ini=1, fim=100):
    print("Downloading databases .........")
    for i in range(ini, fim+1):
        try:
            pag = req.get(f'{URL_DB}/trending/movie/week?api_key={API_KEY}&language=pt-BR&page={i}&include_adult=true')
            json_pag = pag.json()
            data = json_pag['results']
            for dta in data:
                Thread(target=add_movie_id, args=(dta['id'],)).start()
            print("Processing databases .........")
        except:
            continue