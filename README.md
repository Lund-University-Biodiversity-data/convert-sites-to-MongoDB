# convert-sites-to-MongoDB
convert-sites-to-MongoDB_withCentre.py is only for standardrutt. It requires 3 geojson files as input: lines, points and centroids of the square created by them

1. Convert data from zipped shapefiles to geojson format with bulk_shp_to_geojson.sh
2. Format the geojson objects into new json objects to fit the 'site' collection in MongoDB and upload them to Mongo DB with convert-sites-to-MongoDB.py 

<b>Requirements</b>
- Python libraries: json, uuid, pymongo
- GDAL library (to use ogr2ogr function)

<i>To Install Python PyMongo module with pip</i>
```
sudo apt install python-pip
python -m pip install pymongo
```
<i>To enable funtcton ogr2ogr in bulk_shp_to_geojson script</i>
```
sudo apt-get install gdal-bin
```

<b>Executing the script</b>
run in the directory where the zip files are:
```
./bulk_shp_to_geojson.sh
```
```
python convert-sft-sites-to-MongoDB_withCentre.py
```
