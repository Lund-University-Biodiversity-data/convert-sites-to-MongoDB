import json
import uuid
from shapely.geometry import Polygon
import shapely
import numpy as np
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
project = "49f55dc1-a63a-4ebf-962b-4d486db0ab16"
all_polyg = geojson['features']
length = len(all_polyg)

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

    name = all_polyg[index]['properties']['ruta']

    # It should be like below once the ruttnamn is also in the csv file - shp needs to be converted including that field
    # name = all_polyg[index]['properties']['ruta'] + ", " + all_polyg[index]['properties']['ruttnamn']

    location = {
        "siteId": generate_uniqId_format(),
        "name": name,
        "code": all_polyg[index]['properties']['OBJECTID'],
        "status" : "active",
        "type" : "surveyArea",
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