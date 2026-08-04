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

## Terrain / hillshade

The style's `relief` raster-dem source is
`https://tiles.kanardia.eu/terrain/{z}/{x}/{y}.webp` — Web Mercator, 512 px,
Mapbox terrain-RGB encoding (`elevation_m = -10000 + (R*65536 + G*256 + B) *
0.1`), no proxy or reprojection needed.

Zooms 0..14 answer, but 13 and 14 are upstream interpolation of z12 (spot
checked: mean 1.2 m difference from an upsampled z12 parent, no new landforms),
so the source declares `maxzoom: 12` and MapLibre overzooms locally instead of
fetching redundant tiles. Spot checks against Copernicus GLO-90 agree within
~1 m in flat terrain.

Note the unrelated elevation service at `relief.kanardia.eu` is **EPSG:4326
plate carree** (see `/tiles/meta`) and cannot be used as a MapLibre raster-dem
source; use it for elevation queries (`/elevation/path`), not tiles.