## Build tile server

# Download a Geofabrik extract (same source you already use)
'''
wget https://download.geofabrik.de/europe/slovenia-latest.osm.pbf
'''

wget https://github.com/onthegomap/planetiler/releases/latest/download/planetiler.jar

<!-- java -Xmx8g -jar planetiler.jar \
    --osm-path=slovenia-latest.osm.pbf \
    --output=slovenia.mbtiles -->

./scafold

java -Xmx8g -jar planetiler.jar \
    --download \
    --osm-path=slovenia-latest.osm.pbf \
    --output=tiles/ 
    
     # trailing slash / directory path = folder output instead of mbtiles