# convert-sites-to-MongoDB


1. Convert data from zipped shapefiles to geojson format with bulk-shp-to-geojson.sh
2. Convert MongoDB JSON objects and upload them to Mongo DB with convert-sites-to-MongoDB.py 

<b>Requirements</b>
- Python libraries: json, uuid, pymongo

<b>Executing the script</b>
run in the directory where the zip files are:
```
./bulk-shp-to-geojson.sh
```
```
python convert-sites-to-MongoDB
```
