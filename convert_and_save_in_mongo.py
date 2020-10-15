# -*- coding: utf-8 -*-

# import propertiesfile

from pymongo import MongoClient
import datetime
import json
import uuid
import pandas as pd

# set up connection with mongo
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.ecodata
collection = db.site

# open local geojson files
with open('6.geojson') as f:
    transect = json.load(f)

# with open('sit_sites.csv') as f1:
#     attributes = pd.read_csv(f1)

# generate ids for fields in sites
def generate_uniqId_format():
    _uniqid = uuid.uuid4().hex
    indices = [0,8,12,16,20,32]
    parts = [_uniqid[i:j] for i,j in zip(indices, indices[1:])]
    uniqid = '-'.join(parts)
    return uniqid

segments = transect['features']
length = len(segments)

features = []
for index in range(0, length):
    feature = {
        "name": str(index),
        "transectPartId": generate_uniqId_format(),
        "geometry": {
            "type": "LineString",
            "decimalLongitude": segments[index]["geometry"]["coordinates"][0][0],
            "decimalLatitude": segments[index]["geometry"]["coordinates"][0][1],
            "coordinates": segments[index]["geometry"]["coordinates"]
        },
        "length": segments[index]["properties"]["Length"],
        "description": "",
        "type": "none"          
    }
    features.append(feature)

geo_index = {
        "type" : 'Point',
        "coordinates": segments[0]["geometry"]["coordinates"][0]
}

extent_geo = {       
    "type" : 'Point',
    "coordinates": segments[0]["geometry"]["coordinates"][0],
    "decimalLongitude": segments[0]["geometry"]["coordinates"][0][0],
    "decimalLatitude": segments[0]["geometry"]["coordinates"][0][1],
    "areaKmSq": 0,
    "type" : "Point",
    "aream2": 0,
    "centre": [str(segments[0]["geometry"]["coordinates"][0])]
}

location = {
    "siteId": generate_uniqId_format(),
    # "name": attributes['sit_name'],
    "name": "Rökepipan",
    "dateCreated": datetime.datetime.utcnow(),
    "status" : "active",
    "type" : "",
    "isSensitive": True,
    "description": "SEBMS test 1",
    "lastUpdated": datetime.datetime.utcnow(),
    "projects": [
        "a29845ea-893a-46ec-a7e7-a65dbe167708",
        "dab767a5-929e-4733-b8eb-c9113194201f"
        # propertiesfile.projectId
    ],
    "extent": {
        "geometry": extent_geo,
        "source": "Point"
    },
    "geoIndex": geo_index,
    "transectParts": features
}

site_id = collection.insert_one(location).inserted_id
site_id