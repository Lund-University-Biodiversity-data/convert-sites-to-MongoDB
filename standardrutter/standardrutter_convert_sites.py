# -*- coding: utf-8 -*-

# import propertiesfile

# from pymongo import MongoClient
import json
import uuid

# set up connection with mongo
# client = MongoClient()
# client = MongoClient('localhost', 27017)
# db = client.ecodata
# collection = db.site

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

locations = []
# iterate through all sites and save each 
while last <= length:
    features = []
    for index in range(first, last):
        feature_pts = {
            "name": all_pts[index]['properties']['PUNK'],
            "geometry": {
                "type": "Point",
                "decimalLongitude": all_pts[index]["geometry"]["coordinates"][0],
                "decimalLatitude": all_pts[index]["geometry"]["coordinates"][1],
                "coordinates": all_pts[index]["geometry"]["coordinates"]
            },
            "coords_3021": [all_pts[index]["properties"]["xcoord"], all_pts[index]["properties"]["ycoord"]],
            "coords_3006": [all_pts[index]["properties"]["xcoord_2"], all_pts[index]["properties"]["ycoord_2"]],
            "type": "none"            
        }
        feature_lines = {
            "name": all_lines[index]['properties']['LINJE'],
            "geometry": {
                "type": "LineString",
                "coordinates": all_lines[index]["geometry"]["coordinates"][0]
            },
            "Inv1997": all_lines[index]["properties"]["Inv1997"],
            "Inv1998": all_lines[index]["properties"]["Inv1998"],
            "Inv1999": all_lines[index]["properties"]["Inv1999"],
            "Inv2000": all_lines[index]["properties"]["Inv2000"],
            "Inv2001": all_lines[index]["properties"]["Inv2001"],
            "Inv2002": all_lines[index]["properties"]["Inv2002"],
            "Inv2003": all_lines[index]["properties"]["Inv2003"],
            "Inv2004": all_lines[index]["properties"]["Inv2004"],
            "Inv2005": all_lines[index]["properties"]["Inv2005"],
            "Inv2006": all_lines[index]["properties"]["Inv2006"],
            "Inv2007": all_lines[index]["properties"]["Inv2007"],
            "Inv2008": all_lines[index]["properties"]["Inv2008"],
            "type": "none"
        }
        
        features.append(feature_pts)
        features.append(feature_lines)

    extent_geo = {
        "type" : 'Point',
        "coordinates": all_centroids[centroid_index]['geometry']['coordinates'],
        "decimalLongitude": all_centroids[centroid_index]['geometry']['coordinates'][0],
        "decimalLatitude": all_centroids[centroid_index]['geometry']['coordinates'][1],
        "areaKmSq": 0,
        "type" : "Point",
        "aream2": 0,
        "centre": [str(all_centroids[centroid_index]['geometry']['coordinates'][0]), str(all_centroids[centroid_index]['geometry']['coordinates'][1])]
    }
    geo_index = {
        "type" : 'Point',
        "coordinates": all_centroids[centroid_index]['geometry']['coordinates']
    }
    
    location = {
        "siteId": generate_uniqId_format(),
        "gridCode": all_centroids[centroid_index]["properties"]["KARTA"],
        "name": all_centroids[centroid_index]["properties"]["NAMN"],
        "status" : "active",
        "type" : "",
        "isSensitive": True,
        "LAN": all_centroids[centroid_index]["properties"]["LAN"],
        "LSK": all_centroids[centroid_index]["properties"]["LSK"],
        "KartaTx": all_centroids[centroid_index]["properties"]["KartaTx"],
        "area": "0",
        "projects": [
            "89383d0f-9735-4fe7-8eb4-8b2e9e9b7b5c"
        ],
        "extent": {
            "geometry": extent_geo,
            "source": "Point"
        },
        "geoIndex": geo_index,
        "transectParts": features
    }
    locations.append(location)

    first = last
    last = last + 8
    centroid_index = centroid_index + 1

with open('strutt_upload.json', 'w') as f:
    json.dump(locations, f, ensure_ascii=False)