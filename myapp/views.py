from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from myapp.funciones import *
import requests
import request
import json

# Create your views here.
def index(response):
    url = 'https://swapi.co/api/films'
    response = requests.get(url)
    data = response.json()
    peliculas = {'peliculas':[]}
    for i in data['results']:
        id = i['url'].split('/')[-2]
        peliculas['peliculas'].append({'title':i['title'], 'episode_id':i['episode_id'],
         'release_date':i['release_date'], 'director':i['director'],
         'producer':i['producer'], 'id': str(id)})
    return render_to_response('index.html',peliculas)

def movie(response,movie):
    url = 'https://swapi.co/api/films/' + str(movie)
    response = requests.get(url)
    data = response.json()
    movie = {}
    for k,v in data.items():
        if (k == "species" or k == "vehicles" or  k == "url" or
        k == "edited" or k == "created"):
            pass
        elif k == "characters":
            movie[k] = return_names("characters",data,"name")
        elif k == "planets":
            movie[k] = return_names("planets",data,"name")
        elif k == "starships":
            movie[k] = return_names("starships",data,"name")
        else:
            movie[k] = v
    return render_to_response('movie.html', {"movie": movie})

def character(response, character):
    url = 'https://swapi.co/api/people/' + str(character)
    response = requests.get(url)
    data = response.json()
    character = {}
    for k,v in data.items():
        if (k == "edited" or k == "created" or k == "url"):
            pass
        elif k == "starships":
            character[k] = return_names("starships",data,"name")
        elif k == "vehicles":
            character[k] = return_names("vehicles",data,"name")
        elif k == "species":
            character[k] = return_names("species",data,"name")
        elif k == "homeworld":
            names = {}
            response_homeworld = requests.get(v)
            data_homeworld = response_homeworld.json()
            names[data_homeworld["name"]] = v.split('/')[-2]
            character[k] = names
        elif k == "films":
            character[k] = return_names("films",data,"title")
        else:
            character[k] = v
    return render_to_response('character.html', {"character" : character})

def planet(response, planet):
    url = 'https://swapi.co/api/planets/' + str(planet)
    response = requests.get(url)
    data = response.json()
    planet = {}
    for k,v in data.items():
        if (k == "edited" or k == "created" or k == "url"):
            pass
        elif k == "residents":
            planet[k] = return_names("residents",data,"name")
        elif k == "films":
            planet[k] = return_names("films",data,"title")
        else:
            planet[k] = v
    return render_to_response('planet.html', {"planet" : planet})

def starship(response, starship):
    url = 'https://swapi.co/api/starships/' + str(starship)
    response = requests.get(url)
    data = response.json()
    starship = {}
    for k,v in data.items():
        if (k == "edited" or k == "created" or k == "url"):
            pass
        elif k == "pilots":
            starship[k] = return_names("pilots",data,"name")
        elif k == "films":
            starship[k] = return_names("films",data,"title")
        else:
            starship[k] = v
    return render_to_response('starship.html', {"starship" : starship})


@csrf_exempt
def result(request):
    if request.method == 'GET': # If the form is submitted
        search_query = request.GET.get('q', None)

    people_res = return_search("people","name",search_query)

    starships_res = return_search("starships","name",search_query)

    planets_res = return_search("planets","name",search_query)

    films_res = return_search("films","title",search_query)

    query = {"people_res":people_res,"starships_res":starships_res,"planets_res":planets_res,"films_res":films_res}
    return render_to_response('result.html',{'query':query})
