import json
import uuid
from shapely.geometry import Polygon
import shapely
import numpy as np
# import propertiesfile

# open local geojson files
with open('centroider_4326.geojson') as f:
    _centroids = json.load(f)

with open('grid_4326.geojson') as f:
    grid = json.load(f)

# generate ids for fields in sites
def generate_uniqId_format():
    _uniqid = uuid.uuid4().hex
    indices = [0,8,12,16,20,32]
    parts = [_uniqid[i:j] for i,j in zip(indices, indices[1:])]
    uniqid = '-'.join(parts)
    return uniqid

# enter the id of one project this site belongs to
project = "d0b2f329-c394-464b-b5ab-e1e205585a7c"
all_polyg = grid['features']
centroids = _centroids['features']
length = len(all_polyg)

# iterate through all sites and save each 

locations = []
for index in range(0,length):
    polygon_coords = all_polyg[index]["geometry"]["coordinates"][0]
    feature = {
        "geometry": {
            "type": "Polygon",
            "coordinates": polygon_coords
        },
        "type": ""            
    }

    centroid_geom = centroids[index]["geometry"]
    extent_geo = {
        "type" : 'Point',
        "coordinates": centroid_geom["coordinates"],
        "decimalLongitude": centroid_geom["coordinates"][0],
        "decimalLatitude": centroid_geom["coordinates"][1],
        "areaKmSq": 0,
        "type" : "Point",
        "aream2": 0,
        "centre": centroid_geom["coordinates"]
    }
    geo_index = {
        "type" : 'Point',
        "coordinates": centroid_geom["coordinates"]
    }

    location = {
        "siteId": generate_uniqId_format(),
        "name": all_polyg[index]['properties']['BLAD'],
        "gridCode": all_polyg[index]['properties']['BLAD'],
        "status" : "active",
        "type" : "surveyArea",
        "description": "Part of grid 25 x 25",
        "area": "0",
        "projects": [
            project
        ],
        "extent": {
            "geometry": extent_geo,
            "source": "Point"
        },
        "geoIndex": geo_index,
        "transectParts": [feature]
    }

    locations.append(location)

with open('grid_upload.json', 'w') as f:
    json.dump(locations, f)