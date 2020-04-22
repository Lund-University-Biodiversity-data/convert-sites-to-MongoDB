# convert-sites-to-MongoDB


1. Convert data from zipped shapefiles to geojson format with bulk_shp_to_geojson.sh
2. Format the geojson objects into new json objects to fit the 'site' collection in MongoDB and upload them to Mongo DB with convert-sites-to-MongoDB.py 

<b>Requirements</b>
- Python libraries: json, uuid, pymongo

<b>Executing the script</b>
run in the directory where the zip files are:
```
./bulk_shp_to_geojson.sh
```
```
python convert-sites-to-MongoDB
```
