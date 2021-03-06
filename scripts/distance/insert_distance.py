"""
this python files inserts:
1) distances between buildings
2) list of cafeterias in each building
"""

from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost/')
db = client['newb']
col = db['distances']
db.distances.drop()

with open('dist_data.json', 'r', encoding='utf-8') as fp:
    jsonObj = json.load(fp)

    for start in jsonObj:
        for destination in jsonObj[start]:
            col.insert_one({'start': start, 'destination': destination, 'distance': jsonObj[start][destination]})

col = db['buildings']
db.buildings.drop()

with open('locations.json', 'r', encoding='utf-8') as fp:
    jsonObj = json.load(fp)

    dests = jsonObj['destination']
    for dest in dests:
        col.insert_one({'name': dest['building'], 'cafeteria_list': dest['cafeteria_list']})
