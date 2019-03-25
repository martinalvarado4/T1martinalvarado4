from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
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
            names = {}
            for n in data["characters"]:
                response_character = requests.get(n)
                data_character = response_character.json()
                names[data_character["name"]] = n.split('/')[-2]
            movie[k] = names
        elif k == "planets":
            names = {}
            for n in data["planets"]:
                response_planet = requests.get(n)
                data_planet = response_planet.json()
                names[data_planet["name"]] = n.split('/')[-2]
            movie[k] = names
        elif k == "starships":
            names = {}
            for n in data["starships"]:
                response_starship = requests.get(n)
                data_starship = response_starship.json()
                names[data_starship["name"]] = n.split('/')[-2]
            movie[k] = names
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
            names = {}
            for n in data["starships"]:
                response_starships = requests.get(n)
                data_starships = response_starships.json()
                names[data_starships["name"]] = n.split('/')[-2]
            character[k] = names
        elif k == "vehicles":
            names = {}
            for n in data["vehicles"]:
                response_vehicles = requests.get(n)
                data_vehicles = response_vehicles.json()
                names[data_vehicles["name"]] = n.split('/')[-2]
            character[k] = names
        elif k == "species":
            names = {}
            for n in data["species"]:
                response_species = requests.get(n)
                data_species = response_species.json()
                names[data_species["name"]] = n.split('/')[-2]
            character[k] = names
        elif k == "homeworld":
            names = {}
            response_homeworld = requests.get(v)
            data_homeworld = response_homeworld.json()
            names[data_homeworld["name"]] = v.split('/')[-2]
            character[k] = names
        elif k == "films":
            names = {}
            for n in data["films"]:
                response_film = requests.get(n)
                data_film = response_film.json()
                names[data_film["title"]] = n.split('/')[-2]
            character[k] = names
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
            names = {}
            for n in data["residents"]:
                response_residents = requests.get(n)
                data_residents = response_residents.json()
                names[data_residents["name"]] = n.split('/')[-2]
            planet[k] = names
        elif k == "films":
            names = {}
            for n in data["films"]:
                response_film = requests.get(n)
                data_film = response_film.json()
                names[data_film["title"]] = n.split('/')[-2]
            planet[k] = names
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
            names = {}
            for n in data["pilots"]:
                response_pilots = requests.get(n)
                data_pilots = response_pilots.json()
                names[data_pilots["name"]] = n.split('/')[-2]
            starship[k] = names
        elif k == "films":
            names = {}
            for n in data["films"]:
                response_film = requests.get(n)
                data_film = response_film.json()
                names[data_film["title"]] = n.split('/')[-2]
            starship[k] = names
        else:
            starship[k] = v
    return render_to_response('starship.html', {"starship" : starship})


@csrf_exempt
def result(request):
    if request.method == 'GET': # If the form is submitted
        search_query = request.GET.get('q', None)

    url_people = 'https://swapi.co/api/people/?search=' + str(search_query)
    response_people = requests.get(url_people)
    people = response_people.json()
    people_res = {}
    if people["results"] == []:
        pass
    else:
        for i in people["results"]:
            people_res[i["name"]] = i["url"].split('/')[-2]

    url_starship = 'https://swapi.co/api/starships/?search=' + str(search_query)
    response_starships = requests.get(url_starship)
    starships = response_starships.json()
    starships_res = {}
    if starships["results"] == []:
        pass
    else:
        for i in starships["results"]:
            starships_res[i["name"]] = i["url"].split('/')[-2]

    url_planets = 'https://swapi.co/api/planets/?search=' + str(search_query)
    response_planets = requests.get(url_planets)
    planets = response_planets.json()
    planets_res = {}
    if planets["results"] == []:
        pass
    else:
        for i in planets["results"]:
            planets_res[i["name"]] = i["url"].split('/')[-2]

    url_films = 'https://swapi.co/api/films/?search=' + str(search_query)
    response_films = requests.get(url_films)
    films = response_films.json()
    films_res = {}
    if films["results"] == []:
        pass
    else:
        for i in films["results"]:
            films_res[i["title"]] = i["url"].split('/')[-2]

    query = {"people_res":people_res,"starships_res":starships_res,"planets_res":planets_res,"films_res":films_res}
    return render_to_response('result.html',{'query':query})
