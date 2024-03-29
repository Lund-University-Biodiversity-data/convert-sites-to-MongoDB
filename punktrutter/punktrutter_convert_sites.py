
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

source_file_name = 'punktrutter_4326_coords_full.csv'
sorted_file_name = 'punktrutter_sorted.csv'
product_file_name = 'punktrutter_upload.json'
projectId = "b7eee643-d5fe-465e-af38-36b217440bd2"

# open local geojson files
with open(source_file_name) as f:
    all_pts_unsorted = pd.read_csv(f)

all_pts_unsorted.sort_values(by=['persnr','ruttnamn','punkt'], ascending=[True, True, True], inplace=True)

all_pts_unsorted.to_csv(sorted_file_name)

with open(sorted_file_name) as f:
    all_pts = pd.read_csv(f)

# generate ids for fields in sites
def generate_uniqId_format():
    _uniqid = uuid.uuid4().hex
    indices = [0,8,12,16,20,32]
    parts = [_uniqid[i:j] for i,j in zip(indices, indices[1:])]
    uniqid = '-'.join(parts)
    return uniqid


length = len(all_pts)
first = 0
last = 20
print("number of lines in csv file : " + str(length))

date = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
rt90 = osr.SpatialReference()
rt90.ImportFromEPSG(3021)
wgs84  = osr.SpatialReference()
wgs84.ImportFromEPSG(4326)
sweref99  = osr.SpatialReference()
sweref99.ImportFromEPSG(3006)
transformation_to_4326 = osr.CoordinateTransformation(rt90, wgs84)
transformation_to_3006 = osr.CoordinateTransformation(rt90, sweref99)

locations = []

# iterate through all sites and save each 
while last <= length:
    features = []
    coordinates = []
    pointNumber = 1
    for index in range(first, last):
        lng_RT90 = int(all_pts.loc[index]["rt90o"])
        lat_RT90 = int(all_pts.loc[index]["rt90n"])
        lon_wgs84 = all_pts.loc[index]["wgs84_lon"]
        lat_wgs84 = all_pts.loc[index]["wgs84_lat"]
        lng_SWEREF99 = all_pts.loc[index]["sweref99_o"]
        lat_SWEREF99 = all_pts.loc[index]["sweref99_n"]

        if (np.isnan(lon_wgs84)):
            transformed_to_4326 = transformation_to_4326.TransformPoint(lng_RT90, lat_RT90)
            lon_wgs84 = round(float(transformed_to_4326[0]), 7)
            lat_wgs84 = round(float(transformed_to_4326[1]), 7)
        else:
            lon_wgs84 = round(float(lon_wgs84), 7)
            lat_wgs84 = round(float(lat_wgs84), 7)


        if(np.isnan(lat_SWEREF99)):
            transformed_to_3006 = transformation_to_3006.TransformPoint(lng_RT90, lat_RT90)
            lng_SWEREF99 = transformed_to_3006[0]
            lat_SWEREF99 = transformed_to_3006[1]
        else:
            lng_SWEREF99 = lng_SWEREF99
            lat_SWEREF99 = lat_SWEREF99
        
        feature_pts = {
            "internalName": "P" + str(all_pts.loc[index]['punkt']),
            "name": "P" + str(all_pts.loc[index]['punkt']),
            "geometry": {
                "type": "Point",
                "decimalLongitude": round(float(lon_wgs84), 7),
                "decimalLatitude": round(float(lat_wgs84), 7),
                "coordinates": [lon_wgs84, lat_wgs84] 
            },
            "otherCRS": {
                "coords_3021": [lng_RT90, lat_RT90],
                "coords_3006": [lng_SWEREF99, lat_SWEREF99]
            },
            "type": "none",            
        }        
        features.append(feature_pts)
        coordinates.append([lon_wgs84, lat_wgs84])
        pointNumber = pointNumber + 1 

    try :
        polygon = Polygon(coordinates)
        centroid = polygon.centroid
        _centroid_coords = np.array((float(centroid.xy[0][0]), float(centroid.xy[1][0]))) # should be long, lat
        centroid_coords = _centroid_coords.tolist()
    except:
        print("problem with calculating the centroid for " + all_pts.loc[first]["ruttnamn"])
        print(coordinates)

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
        "name": str(all_pts.loc[first]["persnr"]) + "-" + str(all_pts.loc[first]["rnr"]).rjust(2, '0') + " - " + str(all_pts.loc[first]["ruttnamn"]),
        "dateCreated": date,
        "lastUpdated": date,
        "status" : "active",
        "type" : "",
        "kartaTx": all_pts.loc[first]["kartatx"],
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
        "lan": all_pts.loc[first]["lan"],
        "displayProperties": {},
        "adminProperties": {
            "internalSiteId": str(all_pts.loc[first]["persnr"]) + "-" + str(all_pts.loc[first]["rnr"]).rjust(2, '0'),
        }
    }

    km = False if np.isnan(all_pts.loc[first]["km"]) else all_pts.loc[first]["km"]
    description = False if type(all_pts.loc[first]["extra"]) == float else all_pts.loc[first]["extra"]
    if (km):
        location["displayProperties"]["km"] = km
    if (description):
        location["description"] = description

    start = False if np.isnan(all_pts.loc[first]["start"]) else all_pts.loc[first]["start"]
    v1 = False if np.isnan(all_pts.loc[first]["v1"]) else all_pts.loc[first]["v1"]
    v2 = False if np.isnan(all_pts.loc[first]["v2"]) else all_pts.loc[first]["v2"]
    v3 = False if np.isnan(all_pts.loc[first]["v3"]) else all_pts.loc[first]["v3"] 
    v4 = False if np.isnan(all_pts.loc[first]["v4"]) else all_pts.loc[first]["v4"] 
    v5 = False if np.isnan(all_pts.loc[first]["v5"]) else all_pts.loc[first]["v5"] 
    sensom = False if np.isnan(all_pts.loc[first]["sensom"]) else all_pts.loc[first]["sensom"] 
    senvin = False if np.isnan(all_pts.loc[first]["senvin"]) else all_pts.loc[first]["senvin"] 

    if (v1):
        location["adminProperties"]["v1"] = v1
    if (v2):
        location["adminProperties"]["v2"] = v2
    if (v3):
        location["adminProperties"]["v3"] = v3
    if (v4):
        location["adminProperties"]["v4"] = v4
    if (v5):
        location["adminProperties"]["v5"] = v5
    if (sensom):
        location["adminProperties"]["sensom"] = sensom
    if (senvin):
        location["adminProperties"]["senvin"] = senvin
    if (start):
        location["adminProperties"]["start"] = start
        
    locations.append(location)
    pointNumber = 1
    first = last
    last = last + 20

with open(product_file_name, 'w') as f:
    json.dump(locations, f, ensure_ascii=False)

# edit the json to change date to be BSON format by modifying the date string
# if changing the location object above, make sure that this pattern 
# still matches, ie dateCreated is followed by dateUpdated followed by internal - otherwise the date will remain a string and other values will be broken
with open(product_file_name, 'r') as f:
    text = f.read()
    text = text.replace('dateCreated": "2', 'dateCreated": ISODate("2')
    text = text.replace('lastUpdated": "2', 'lastUpdated": ISODate("2')
    text = text.replace('", "lastUpdated', '"), "lastUpdated')
    text = text.replace('", "status', '"), "status')
    f.close()

with open(product_file_name, 'w') as f:
    f.write(text)

print('mongoimport --jsonArray --db ecodata --collection site --file punktrutter_upload.json')
