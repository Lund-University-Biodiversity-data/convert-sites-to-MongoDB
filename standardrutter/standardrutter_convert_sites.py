
import json
import uuid

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
        pts_geometry = all_pts[index]["geometry"]["coordinates"]
        pts_props = [all_pts[index]["properties"]
        feature_pts = {
            "name": all_pts[index]['properties']['PUNK'],
            "geometry": {
                "type": "Point",
                "decimalLongitude": pts_geometry[0],
                "decimalLatitude": pts_geometry[1],
                "coordinates": pts_geometry
            },
            "coords_3021":pts_props["xcoord"], all_pts[index]["properties"]["ycoord"]],
            "coords_3006":pts_props["xcoord_2"], all_pts[index]["properties"]["ycoord_2"]],
            "type": "none"            
        }
        lines_geometry = all_lines[index]["geometry"]
        lines_props = all_lines[index]["properties"]
        feature_lines = {
            "name": all_lines[index]['properties']['LINJE'],
            "geometry": {
                "type": "LineString",
                "coordinates": lines_geometry["coordinates"][0]
            },
            "Inv1997": lines_props["Inv1997"],
            "Inv1998": lines_props["Inv1998"],
            "Inv1999": lines_props["Inv1999"],
            "Inv2000": lines_props["Inv2000"],
            "Inv2001": lines_props["Inv2001"],
            "Inv2002": lines_props["Inv2002"],
            "Inv2003": lines_props["Inv2003"],
            "Inv2004": lines_props["Inv2004"],
            "Inv2005": lines_props["Inv2005"],
            "Inv2006": lines_props["Inv2006"],
            "Inv2007": lines_props["Inv2007"],
            "Inv2008": lines_props["Inv2008"],
            "type": "none"
        }
        
        features.append(feature_pts)
        features.append(feature_lines)
        
    centroid_geometry = all_centroids[centroid_index]['geometry']
    centroid_props = all_centroids[centroid_index]["properties"]
    extent_geo = {
        "type" : 'Point',
        "coordinates": centroid_geometry['coordinates'],
        "decimalLongitude": centroid_geometry['coordinates'][0],
        "decimalLatitude": centroid_geometry['coordinates'][1],
        "areaKmSq": 0,
        "type" : "Point",
        "aream2": 0,
        "centre": [str(centroid_geometry['coordinates'][0]), str(centroid_geometry['coordinates'][1])]
    }
    geo_index = {
        "type" : 'Point',
        "coordinates": centroid_geometry['coordinates']
    }
    
    location = {
        "siteId": generate_uniqId_format(),
        "gridCode": centroid_props["KARTA"],
        "name": centroid_props["NAMN"],
        "status" : "active",
        "type" : "",
        "isSensitive": True,
        "LAN": centroid_props["LAN"],
        "LSK": centroid_props["LSK"],
        "KartaTx": centroid_props["KartaTx"],
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