from pymongo import MongoClient
import datetime
import json
import uuid

# set up connection with mongo
client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.ecodata
collection = db.site

# open local geojson files
with open('skane_pts.geojson') as f:
    data_pts = json.load(f)

with open('skane_lines.geojson') as f1:
    data_lines = json.load(f1)

# generate ids for fields in sites
def generate_uniqId_format():
    _uniqid = uuid.uuid4().hex
    indices = [0,8,12,16,20,32]
    parts = [_uniqid[i:j] for i,j in zip(indices, indices[1:])]
    uniqid = '-'.join(parts)
    return uniqid


all_pts = data_pts['features']
all_lines = data_lines['features']
length = len(all_pts)
first = 0
last = 8

# iterate through all sites and save each 
while last <= length:
    features = []
    for index in range(first, last):
        feature_pts = {
            "name": all_pts[index]['properties']['PUNK'],
            "poiId": generate_uniqId_format(),
            "geometry": {
                "type": "Point",
                "decimalLongitude": all_pts[index]["geometry"]["coordinates"][0],
                "decimalLatitude": all_pts[index]["geometry"]["coordinates"][1],
                "coordinates": all_pts[index]["geometry"]["coordinates"]
            },
            "description": "",
            "type": "survey"            
        }
        feature_lines = {
            "name": all_lines[index]['properties']['LINJE'],
            "poiId": generate_uniqId_format(),
            "geometry": {
                "type": "LineString",
                "decimalLongitude": all_lines[index]["geometry"]["coordinates"][0],
                "decimalLatitude": all_lines[index]["geometry"]["coordinates"][1],
                "coordinates": all_lines[index]["geometry"]["coordinates"]
            },
            "description": "",
            "type": "survey"
        }
        
        features.append(feature_pts)
        features.append(feature_lines)

    extent_geo = {
        "type" : all_pts[first]['geometry']['type'],
        "coordinates": all_pts[first]['geometry']['coordinates'],
        "decimalLongitude": all_pts[first]['geometry']['coordinates'][0],
        "decimalLatitude": all_pts[first]['geometry']['coordinates'][1],
        "areaKmSq": 0,
        "datum" : "",
        "fid" : "",
        "precision" : "",
        "lga" : "",
        "bbox" : "",
        "nrm" : "",
        "locality" : "",
        "pid" : "",
        "mvs" : "",
        "uncertainty" : "",
        "type" : "Point",
        "state" : "",
        "layerName" : "",
        "radius" : "",
        "mvg" : "",
        "aream2": 0,
        "centre": [str(all_pts[first]['geometry']['coordinates'][0]), str(all_pts[first]['geometry']['coordinates'][1])]
    }
    geo_index = {
        "type" : all_pts[first]['geometry']['type'],
        "coordinates": all_pts[first]['geometry']['coordinates']
    }
    
    location = {
        "siteId": generate_uniqId_format(),
        "name": all_pts[first]["properties"]["KARTA"],
        "dateCreated": datetime.datetime.utcnow(),
        "status" : "active",
        "type" : "surveyArea",
        "description": "standard route test",
        "lastUpdated": datetime.datetime.utcnow(),
        "area": "0",
        "externalId": "",
        "notes": "",
        "projects": [
            "1e62b24d-b9de-480a-9d87-585d3a404544"
        ],
        "extent": {
            "geometry": extent_geo,
            "source": "Point"
        },
        "geo_index": geo_index,
        "poi": features
    }

    first = last
    last = last + 8

    site_id = collection.insert_one(location).inserted_id
    site_id
   
    