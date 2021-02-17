import datetime
import pandas as pd
import json
import uuid
from shapely.geometry import Polygon
import numpy as np
try:
    from osgeo import osr
except:
    sys.exit('ERROR: cannot find OSR module')

# The project ID might need to be changed some time
projectId = "d0b2f329-c394-464b-b5ab-e1e205585a7c" # nattrutt on prod

# open local geojson files
with open('NattPOSITIONSMASTER.csv') as f:
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

locations = []
rt90 = osr.SpatialReference()
rt90.ImportFromEPSG(3021)
wgs84  = osr.SpatialReference()
wgs84.ImportFromEPSG(4326)
transformation = osr.CoordinateTransformation(rt90,wgs84)

# iterate through all sites and save each 
while last <= length:
    features = []
    coordinates = []
    for index in range(first, last):
        lng_RT90 = all_pts.loc[index]["RT-90 O"]
        lat_RT90 = all_pts.loc[index]["RT-90 N"]
        transformed = transformation.TransformPoint(lng_RT90, lat_RT90)
        x_coordinate = round(transformed[0], 6)
        y_coordinate = round(transformed[1], 6)
        
        if (pd.isna(all_pts.loc[index]["PUNKTBESKRIVNING"]) == False):
            description = all_pts.loc[index]["PUNKTBESKRIVNING"] 
        else:
            description = ""

        if (pd.isna(all_pts.loc[index]['PUNKTNAMN']) == False):
            point_name = str(all_pts.loc[index]['Punkt']) + " - " + str(all_pts.loc[index]['PUNKTNAMN'])
        else: 
            point_name = str(all_pts.loc[index]['Punkt'])

        feature_pts = {
            "name": point_name, 
            "description": description,
            "geometry": {
                "type": "Point",
                "decimalLongitude": float(x_coordinate),
                "decimalLatitude": float(y_coordinate),
                "coordinates": [x_coordinate, y_coordinate] 
            },
            "coords_3021": [lng_RT90, lat_RT90],
            "type": "none"            
        }        
        features.append(feature_pts)
        coordinates.append([x_coordinate, y_coordinate]) 

    polygon = Polygon(coordinates)
    centroid = polygon.centroid
    _centroid_coords = np.array((round(float(centroid.xy[0][0]), 6), round(float(centroid.xy[1][0])), 6)) # should be long, lat
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

    if (pd.isna(all_pts.loc[first]["ÅR"])):
        print(all_pts.loc[first]["ÅR"])
        start = 0
    else:
        start = int(all_pts.loc[first]["ÅR"])

    name = all_pts.loc[first]["RUTT"] 
    commonName = ""
    
    if (pd.isna(all_pts.loc[first]["RUTTNAMN"]) == False) :
        name = name + ", " + all_pts.loc[first]["RUTTNAMN"]
        commonName = all_pts.loc[first]["RUTTNAMN"]

    location = {
        "siteId": generate_uniqId_format(),
        "name": name,
        "commonName": commonName,
        "status" : "active",
        "type" : "",
        "description": description,
        "kartaTx": all_pts.loc[first]["RUTT"],
        "area": "0",
        "projects": [
            projectId
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
