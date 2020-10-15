
import datetime
import pandas as pd
import json
import uuid
from shapely.geometry import Polygon
import numpy as np

# open local geojson files
with open('punktrutter_4326_coords.csv') as f:
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
        feature_pts = {
            "name": str(all_pts.loc[index]['punkt']),
            "geometry": {
                "type": "Point",
                "decimalLongitude": float(all_pts.loc[index]["wgs84_lon"]),
                "decimalLatitude": float(all_pts.loc[index]["wgs84_lat"]),
                "coordinates": [all_pts.loc[index]["wgs84_lon"], all_pts.loc[index]["wgs84_lat"]] 
            },
            "type": "none"            
        }        
        features.append(feature_pts)
        coordinates.append([all_pts.loc[index]["wgs84_lon"], all_pts.loc[index]["wgs84_lat"]]) 

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
    
    if (type(all_pts.loc[first]["extra"]) == float):
        description = ""
    else:
        description = all_pts.loc[first]["extra"] 

    location = {
        "siteId": generate_uniqId_format(),
        "name": all_pts.loc[first]["ruttnamn"],
        "status" : "active",
        "type" : "",
        "description": description,
        "KartaTx": all_pts.loc[first]["kartatx"],
        "area": "0",
        "projects": [
            "dab767a5-929e-4733-b8eb-c9113194201f"
        ],
        "extent": {
            "geometry": extent_geo,
            "source": "Point"
        },
        "geoIndex": geo_index,
        "transectParts": features,
        "yearStarted": int(all_pts.loc[first]["start"])
    }
    locations.append(location)
    first = last
    last = last + 20

with open('punktrutter_upload1.json', 'w') as f:
    json.dump(locations, f, ensure_ascii=False)
