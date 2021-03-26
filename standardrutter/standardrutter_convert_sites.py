
import json
import uuid
import datetime

# punkter och linjer should contain coordinates with additional CRS

# open local geojson files
with open('/home/aleksandra/Documents/Data/sft/strutt_data_for_mongo/punkter.geojson') as f:
    data_pts = json.load(f)

with open('/home/aleksandra/Documents/Data/sft/strutt_data_for_mongo/linjer.geojson') as f1:
    data_lines = json.load(f1)

with open('/home/aleksandra/Documents/Data/sft/strutt_data_for_mongo/centroider.geojson') as f2:
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
# ID of standardrutt project on production
projectId = "89383d0f-9735-4fe7-8eb4-8b2e9e9b7b5c"
length = len(all_pts)
first = 0
last = 8
centroid_index = 0
date = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
locations = []

# iterate through all sites and save each as a separate object in locations array
while last <= length:
    features = []
    for index in range(first, last):
        pts_geometry = all_pts[index]["geometry"]["coordinates"]
        pts_props = all_pts[index]["properties"]
        pts_x_coord_3021 = round(float(pts_props["xcoord"]), 6)
        pts_y_coord_3021 = round(float(pts_props["ycoord"]), 6)
        pts_x_coord_3006 = round(float(pts_props["xcoord_2"]), 6)
        pts_y_coord_3006 = round(float(pts_props["ycoord_2"]), 6)

        pts_lng_coord_4326 = round(float(pts_geometry[0]), 7)
        pts_lat_coord_4326 = round(float(pts_geometry[1]), 7)

        # prepare points
        feature_pts = {
            "name": pts_props['PUNK'],
            "geometry": {
                "type": "Point",
                "decimalLongitude": pts_lng_coord_4326,
                "decimalLatitude": pts_lat_coord_4326,
                "coordinates": [pts_lng_coord_4326, pts_lat_coord_4326]
            },
            "otherCRS": {
                "coords_3021":[pts_x_coord_3021, pts_y_coord_3021],
                "coords_3006":[pts_x_coord_3006, pts_y_coord_3006]
            },
            "type": "none",
            "adminProperties": {
                "Inv1996" : pts_props["Inv1996"],
                "Inv1997" : pts_props["Inv1997"],
                "Inv1998" : pts_props["Inv1998"],
                "Inv1999" : pts_props["Inv1999"],
                "Inv2000" : pts_props["Inv2000"],
                "Inv2001" : pts_props["Inv2001"],
                "Inv2002" : pts_props["Inv2002"],
                "Inv2003" : pts_props["Inv2003"],
                "Inv2004" : pts_props["Inv2004"],
                "Inv2004" : pts_props["Inv2004"],
                "Inv2005" : pts_props["Inv2005"],
                "Inv2006" : pts_props["Inv2006"],
                "Inv2007" : pts_props["Inv2007"],
                "Inv2008" : pts_props["Inv2008"]
            }            
        }

        # prepare lines
        lines_geometry = all_lines[index]["geometry"]
        lines_props = all_lines[index]["properties"]
        _coords_shorter_1 = map(lambda x: round(x, 5), lines_geometry["coordinates"][0][0])
        _coords_shorter_2 = map(lambda x: round(x, 5), lines_geometry["coordinates"][0][1])
        coords_shorter_1 = list(_coords_shorter_1)
        coords_shorter_2 = list(_coords_shorter_2)
        coords_shorter = [coords_shorter_1, coords_shorter_2]
        feature_lines = {
            "name": lines_props['LINJE'],
            "geometry": {
                "type": "LineString",
                "coordinates": coords_shorter
            },
            "displayProperties": {},
            "adminProperties": {
                "Inv1996" : lines_props["Inv1996"],
                "Inv1997" : lines_props["Inv1997"],
                "Inv1998" : lines_props["Inv1998"],
                "Inv1999" : lines_props["Inv1999"],
                "Inv2000" : lines_props["Inv2000"],
                "Inv2001" : lines_props["Inv2001"],
                "Inv2002" : lines_props["Inv2002"],
                "Inv2003" : lines_props["Inv2003"],
                "Inv2004" : lines_props["Inv2004"],
                "Inv2004" : lines_props["Inv2004"],
                "Inv2005" : lines_props["Inv2005"],
                "Inv2006" : lines_props["Inv2006"],
                "Inv2007" : lines_props["Inv2007"],
                "Inv2008" : lines_props["Inv2008"]
            },         
            "type": "none"
        }
        
        features.append(feature_pts)
        features.append(feature_lines)
        
    centroid_geometry = all_centroids[centroid_index]['geometry']
    centroid_props = all_centroids[centroid_index]['properties']
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

    lines_props_for_extent = all_lines[first]["properties"]
    name = centroid_props["karta"] + " - " + lines_props_for_extent["NAMN"]

    if (centroid_props["karta"] != lines_props_for_extent["KARTA"]):
        print("centroid not matching line!")

    location = {
        "siteId": generate_uniqId_format(),
        "dateCreated": date,
        "lastUpdated": date,
        "karta": centroid_props["karta"],
        "name": name,
        "commonName": lines_props_for_extent["NAMN"],
        "status" : "active",
        "type" : "",
        "bookedBy": "",
        "isSensitive": True,
        "LAN": lines_props_for_extent["LAN"],
        "LSK": lines_props_for_extent["LSK"],
        "kartaTx": lines_props_for_extent["KartaTx"],
        "area": "0",
        "projects": [
            projectId
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
with open('strutt_upload.json', 'r') as f:
    text = f.read()
    text = text.replace('dateCreated": "2', 'dateCreated": ISODate("2')
    text = text.replace('lastUpdated": "2', 'lastUpdated": ISODate("2')
    text = text.replace('", "karta"', '"), "karta"')
    text = text.replace('", "lastUpdated', '"), "lastUpdated')
    f.close()

with open('strutt_upload.json', 'w') as f:
    f.write(text)