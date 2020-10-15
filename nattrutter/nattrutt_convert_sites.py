import datetime
import pandas as pd
import json
import uuid
from shapely.geometry import Polygon
import numpy as np

# open local geojson files
with open('nattrutt_4326_coords.csv') as f:
    all_pts = pd.read_csv(f)

# generate ids for fields in sites
def generate_uniqId_format():
    _uniqid = uuid.uuid4().hex
    indices = [0,8,12,16,20,32]
    parts = [_uniqid[i:j] for i,j in zip(indices, indices[1:])]
    uniqid = '-'.join(parts)
    return uniqid


length = len(all_pts.index)
first = 0
last = 20
print(length)

locations = []

# iterate through all sites and save each 
while last <= length:
    features = []
    coordinates = []
    for index in range(first, last):
        if (type(all_pts.loc[index]["PUNKTBESKR"]) == float):
            description = ""
        else:
            description = all_pts.loc[index]["PUNKTBESKR"] 

        if (type(all_pts.loc[index]['PUNKTNAMN']) == float):
            point_name = str(all_pts.loc[index]['Punkt'])
        else: 
            point_name = str(all_pts.loc[index]['Punkt']) + " - " + str(all_pts.loc[index]['PUNKTNAMN'])

        feature_pts = {
            "name": point_name, 
            "description": description,
            "geometry": {
                "type": "Point",
                "decimalLongitude": float(all_pts.loc[index]["xcoord"]),
                "decimalLatitude": float(all_pts.loc[index]["ycoord"]),
                "coordinates": [all_pts.loc[index]["xcoord"], all_pts.loc[index]["ycoord"]] 
            },
            "type": "none"            
        }        
        features.append(feature_pts)
        coordinates.append([all_pts.loc[index]["xcoord"], all_pts.loc[index]["ycoord"]]) 

    polygon = Polygon(coordinates)
    centroid = polygon.centroid
    _centroid_coords = np.array((float(centroid.xy[0][0]), float(centroid.xy[1][0]))) # should be long, lat
    centroid_coords = _centroid_coords.tolist()

    extent_geo = {
        "type" : 'Point',
        "coordinates": centroid_coords,
        "decimalLongitude": centroid_coords[0],
        "decimalLatitude": centroid_coords[1],
        "areaKmSq": 0,
        "type" : "Point",
        "aream2": 0,
        "centre": centroid_coords
    }
    geo_index = {
        "type" : "Point",
        "coordinates": centroid_coords
    }

    if (type(all_pts.loc[first]["ÅR"]) == float):
        start = 0
    else:
        start = all_pts.loc[first]["ÅR"]

    if (type(all_pts.loc[first]["RUTTNAMN"]) == float):
        name = ""
    else:
        name = all_pts.loc[first]["RUTTNAMN"]
    location = {
        "siteId": generate_uniqId_format(),
        "name": name,
        "status" : "active",
        "type" : "",
        "description": description,
        "KartaTx": all_pts.loc[first]["RUTT"],
        "area": "0",
        "projects": [
            "d0b2f329-c394-464b-b5ab-e1e205585a7c" # nattrutt on prod
        ],
        "extent": {
            "geometry": extent_geo,
            "source": "Point"
        },
        "geoIndex": geo_index,
        "transectParts": features,
        "yearStarted": start
    }
    locations.append(location)
    first = last
    last = last + 20

with open('natrutter_upload.json', 'w') as f:
    json.dump(locations, f, ensure_ascii=False)
