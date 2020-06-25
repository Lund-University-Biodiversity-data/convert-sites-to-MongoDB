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
with open('punkter.geojson') as f:
    data_pts = json.load(f)

with open('linjer.geojson') as f1:
    data_lines = json.load(f1)

with open('centroider.geojson') as f2:
    data_extent = json.load(f2)

# generate ids for fields in sites
def generate_uniqId_format():
    _uniqid = uuid.uuid4().hex
    indices = [0,8,12,16,20,32]
    parts = [_uniqid[i:j] for i,j in zip(indices, indices[1:])]
    uniqid = '-'.join(parts)
    return uniqid


all_pts = data_pts['features']
all_lines = data_lines['features']
all_centroids = data_extent['features']
length = len(all_pts)
first = 0
last = 8
centroid_index = 0

# iterate through all sites and save each 
while last <= length:
    features = []
    for index in range(first, last):
        feature_pts = {
            "name": all_pts[index]['properties']['PUNK'],
            "transectPartId": generate_uniqId_format(),
            "geometry": {
                "type": "Point",
                "decimalLongitude": all_pts[index]["geometry"]["coordinates"][0],
                "decimalLatitude": all_pts[index]["geometry"]["coordinates"][1],
                "coordinates": all_pts[index]["geometry"]["coordinates"]
            },
            "description": "",
            "type": "none"            
        }
        feature_lines = {
            "name": all_lines[index]['properties']['LINJE'],
            "transectPartId": generate_uniqId_format(),
            "geometry": {
                "type": "LineString",
                "decimalLongitude": all_lines[index]["geometry"]["coordinates"][0],
                "decimalLatitude": all_lines[index]["geometry"]["coordinates"][1],
                "coordinates": all_lines[index]["geometry"]["coordinates"]
            },
            "description": "",
            "type": "none"
        }
        
        features.append(feature_pts)
        features.append(feature_lines)
        print("features are: " +str(len(feature_pts)))

    extent_geo = {
        "type" : 'Point',
        "coordinates": all_centroids[centroid_index]['geometry']['coordinates'],
        "decimalLongitude": all_centroids[centroid_index]['geometry']['coordinates'][0],
        "decimalLatitude": all_centroids[centroid_index]['geometry']['coordinates'][1],
        "areaKmSq": 0,
        "type" : "Point",
        "aream2": 0,
        "center": [str(all_centroids[centroid_index]['geometry']['coordinates'][0]), str(all_centroids[centroid_index]['geometry']['coordinates'][1])]
    }
    geo_index = {
        "type" : 'Point',
        "coordinates": all_centroids[centroid_index]['geometry']['coordinates']
    }
    
    location = {
        "siteId": generate_uniqId_format(),
        "name": all_centroids[centroid_index]["properties"]["KARTA"],
        "dateCreated": datetime.datetime.utcnow(),
        "status" : "active",
        "type" : "",
        "isSensitive": True,
        "description": "standard route test 2",
        "lastUpdated": datetime.datetime.utcnow(),
        "area": "0",
        "externalId": "",
        "projects": [
            "dab767a5-929e-4733-b8eb-c9113194201f"
        ],
        "extent": {
            "geometry": extent_geo,
            "source": "Point"
        },
        "geo_index": geo_index,
        "transectParts": features
    }
    first = last
    last = last + 8
    centroid_index = centroid_index + 1

    site_id = collection.insert_one(location).inserted_id
    site_id