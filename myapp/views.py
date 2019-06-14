from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from myapp.funciones import *
import requests
import request
import json

# Create your views here.
def index(response):
    url = "https://swapi-graphql-integracion-t3.herokuapp.com"
    query = {"query": "{allFilms { edges { node { id title releaseDate director producers episodeID }}}}"}
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(query), headers=headers)
    data = response.json()["data"]
    peliculas = {'peliculas': []}
    for p in data['allFilms']['edges']:
        pelicula = p['node']
        peliculas['peliculas'].append({'title': pelicula['title'], 'episode_id': pelicula['episodeID'],
                                      'release_date': pelicula['releaseDate'], 'director': pelicula['director'],
                                      'producer': pelicula['producers'], 'id': pelicula['id']})
    return render_to_response('index.html', peliculas)

def movie(response, movie):
    url = "https://swapi-graphql-integracion-t3.herokuapp.com"
    query = {"query": "{film(id: \""+movie+"\") {title id episodeID openingCrawl director producers releaseDate characterConnection {characters {name id}}planetConnection{planets{name id}}starshipConnection{starships{name id}}}}"}
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(query), headers=headers)
    data = response.json()["data"]
    movie = {}
    movie["title"] = data["film"]["title"]
    movie["episodeID"] = data["film"]["episodeID"]
    movie["openingCrawl"] = data["film"]["openingCrawl"]
    movie["director"] = data["film"]["director"]
    movie["producers"] = data["film"]["producers"]
    movie["releaseDate"] = data["film"]["releaseDate"]
    movie["characters"] = data["film"]["characterConnection"]["characters"]
    movie["planets"] = data["film"]["planetConnection"]["planets"]
    movie["starships"] = data["film"]["starshipConnection"]["starships"]
    return render_to_response('movie.html', {"movie": movie})

def character(response, character):
    url = "https://swapi-graphql-integracion-t3.herokuapp.com"
    query = {"query": "{person(id: \""+character+"\"){ name height mass hairColor skinColor eyeColor birthYear gender homeworld {id name}filmConnection{films{title id}} starshipConnection{starships{name id}}}}"}
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(query), headers=headers)
    data = response.json()["data"]["person"]
    character = {}
    for k,v in data.items():
        if k == "starshipConnection":
            character["starships"] = v["starships"]
        elif k == "vehicleConnection":
            character["vehicles"] = v["vehicles"]
        elif k == "species":
            character[k] = v
        elif k == "homeworld":
            character[k] = v
        elif k == "filmConnection":
            character["films"] = v["films"]
        else:
            character[k] = v
    print(character)
    return render_to_response('character.html', {"character" : character})

def planet(response, planet):
    url = "https://swapi-graphql-integracion-t3.herokuapp.com"
    query = {"query": "{planet(id: \""+ planet +"\"){ name rotationPeriod orbitalPeriod diameter climates gravity terrains surfaceWater population residentConnection{residents{id name}}filmConnection{films{title id}}}}"}
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(query), headers=headers)
    data = response.json()["data"]["planet"]
    planet = {}
    for k,v in data.items():
        if k == "residentConnection":
            planet["residents"] = v["residents"]
        elif k == "filmConnection":
            planet["films"] = v["films"]
        else:
            planet[k] = v
    return render_to_response('planet.html', {"planet" : planet})

def starship(response, starship):
    url = "https://swapi-graphql-integracion-t3.herokuapp.com"
    query = {"query": "{ starship(id: \""+starship+"\"){ name model manufacturers costInCredits length maxAtmospheringSpeed crew passengers cargoCapacity consumables hyperdriveRating MGLT starshipClass pilotConnection{pilots{name id}}filmConnection{films{title id}}}}"}
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(query), headers=headers)
    data = response.json()["data"]["starship"]
    starship = {}
    for k,v in data.items():
        if k == "pilotConnection":
            starship["pilots"] = v["pilots"]
        elif k == "filmConnection":
            starship["films"] = v["films"]
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
