import uuid
from shapely.geometry import Polygon, LineString
import numpy as np
import pandas as pd
import json
# import propertiesfile

# open local geojson files
with open('spatial_data_geojson_sebms.csv') as f:
    sites = pd.read_csv(f)

with open('persons_with_sites.csv') as f1:
    persons = pd.read_csv(f1)


# generate ids for fields in sites
def generate_uniqId_format():
    _uniqid = uuid.uuid4().hex
    indices = [0,8,12,16,20,32]
    parts = [_uniqid[i:j] for i,j in zip(indices, indices[1:])]
    uniqid = '-'.join(parts)
    return uniqid

# enter the id of one project this site belongs to
projectId = "30634be4-7aac-4ffb-8e5f-5e100ed2a4ea" # propertiesfile.projectId

transects = sites.groupby('site_name')
# iterate through all sites and save each in locations list
locations = []

for name, segment in transects:
    # find persons who have this site assigned to them and store them in site object
    bookedByPersons = persons[persons['site_name'] == name]['personId']
    bookedBy = []
    for person in bookedByPersons:
        bookedBy.append(person)

    # group segments by the site they belong to
    group = transects.get_group(name)

    # iterate all transect parts/ segments and save each in segments list to save in site.transectParts
    segments = []

    # save each coordinate pair separately to calculate centroid below
    coordinates = []
    for index, row in group.iterrows():

        feature_geometry = json.loads(group.loc[index]['epsg3006geom'])

        feature = {
            "name": str(group.loc[index]['segment']), 
            "geometry": {
                "type": feature_geometry.get("type"),
                "coordinates": feature_geometry.get("coordinates") 
            },
            "type": "none",
            "seg_uid": str(group.loc[index]['seg_uid'])            
        }        
        segments.append(feature)

        # arrays have different levels of nesting depending on geometry type so unpack them correctly to get each point
        if (feature_geometry.get("type")) == 'LineString':
            for point in feature_geometry.get("coordinates"):
                coordinates.append(point) 
        elif (feature_geometry.get("type") == 'Polygon' or feature_geometry.get("type") == 'MultiLineString'):
            for point in feature_geometry.get("coordinates")[0]:
                coordinates.append(point) 
        else:
            print("problem" + str(feature["name"]))


    if (len(coordinates) > 2):
        polygon = Polygon(coordinates)
    else:
        polygon = LineString(coordinates)
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

    location = {
        "siteId": generate_uniqId_format(),
        "name": name,
        "status" : "active",
        "type" : "",
        "area": "0",
        "projects": [
            projectId
        ],
        "extent": {
            "geometry": extent_geo,
            "source": "Point"
        },
        "geoIndex": geo_index,
        "transectParts": segments,
        "bookedBy": bookedBy
    }
    locations.append(location)

with open('slinga_upload.json', 'w') as f:
    json.dump(locations, f, ensure_ascii=False)
