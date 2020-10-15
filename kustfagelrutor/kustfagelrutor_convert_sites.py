import json
import uuid
from shapely.geometry import Polygon
import shapely
import numpy as np
import json
# import propertiesfile

# open local geojson files
with open('kustfagel_4326_coords.geojson') as f:
    geojson = json.load(f)


# generate ids for fields in sites
def generate_uniqId_format():
    _uniqid = uuid.uuid4().hex
    indices = [0,8,12,16,20,32]
    parts = [_uniqid[i:j] for i,j in zip(indices, indices[1:])]
    uniqid = '-'.join(parts)
    return uniqid

# enter the id of one project this site belongs to
project = "dab767a5-929e-4733-b8eb-c9113194201f" # propertiesfile.projectId
all_polyg = geojson['features']
length = 50

# iterate through all sites and save each 

locations = []
for index in range(0,length):
    polygon_coords = all_polyg[index]["geometry"]["coordinates"][0]
    feature = {
        "geometry": {
            "type": "Polygon",
            "coordinates": all_polyg[index]["geometry"]["coordinates"][0]
        },
        "type": ""            
    }

    polygon = Polygon(polygon_coords[0])
    centroid = polygon.centroid

    _centroid_coords = np.array((centroid.xy[0][0], centroid.xy[1][0])) # should be long, lat
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
        "type" : 'Point',
        "coordinates": centroid_coords
    }

    location = {
        "siteId": generate_uniqId_format(),
        "name": all_polyg[index]['properties']['ruta'],
        "code": all_polyg[index]['properties']['OBJECTID'],
        "status" : "active",
        "type" : "surveyArea",
        "description": "Archipelago test",
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

with open('kustfagelrutor_upload.json', 'w') as f:
    json.dump(locations, f)