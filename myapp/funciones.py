from django.shortcuts import render, render_to_response
import requests
import request
import json

def return_names(type, data, key):
    names = {}
    for n in data[type]:
        response = requests.get(n)
        data_res = response.json()
        names[data_res[key]] = n.split('/')[-2]
    return names

def return_search(type, key, search_query):
    url = 'https://swapi.co/api/{}/?search='.format(type) + str(search_query)
    response = requests.get(url)
    data = response.json()
    data_res = {}
    while data["next"] != None:
        if data["results"] == []:
            pass
        else:
            for i in data["results"]:
                data_res[i[key]] = i["url"].split('/')[-2]
        url = data["next"]
        response = requests.get(url)
        data = response.json()
    if data["results"] == []:
        pass
    else:
        for i in data["results"]:
            data_res[i[key]] = i["url"].split('/')[-2]
    return data_res
