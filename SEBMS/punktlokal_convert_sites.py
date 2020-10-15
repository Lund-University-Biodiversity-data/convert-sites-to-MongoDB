import datetime
import json
import uuid
import pandas as pd

# open local geojson files
with open('point_4326_coords.geojson') as f:
    transect = json.load(f)

# generate ids for fields in sites
def generate_uniqId_format():
    _uniqid = uuid.uuid4().hex
    indices = [0,8,12,16,20,32]
    parts = [_uniqid[i:j] for i,j in zip(indices, indices[1:])]
    uniqid = '-'.join(parts)
    return uniqid

points = transect['features']
length = len(points)

locations = []
for index in range(0, length):

    geo_index = {
            "type" : 'Point',
            "coordinates": points[index]["geometry"]["coordinates"]
    }

    extent_geo = {       
        "type" : 'Point',
        "coordinates": points[index]["geometry"]["coordinates"],
        "decimalLongitude": points[index]["geometry"]["coordinates"][0],
        "decimalLatitude": points[index]["geometry"]["coordinates"][1],
        "areaKmSq": 0,
        "type" : "Point",
        "aream2": 0,
        "centre": points[index]["geometry"]["coordinates"]
    }

    location = {
        "siteId": generate_uniqId_format(),
        "name": points[index]["properties"]["sit_name"],
        "status" : "active",
        "type" : "",
        "isSensitive": False,
        "description": points[index]["properties"]["sit_commen"],
        "projects": [
            "1e62b24d-b9de-480a-9d87-585d3a404544"
        ],
        "transectParts": [],
        "extent": {
            "geometry": extent_geo,
            "source": "Point"
        },
        "geoIndex": geo_index
        }
    locations.append(location)

print(locations[0])

with open('point_upload.json', 'w') as f:
    json.dump(locations, f)