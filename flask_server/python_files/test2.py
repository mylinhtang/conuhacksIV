import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import os

# Check if the Montreal borough shapefile exists
borough_shapefile = '/limites-administratives-agglomeration-nad83.shp'
if not os.path.exists(borough_shapefile):
    print(f"Error: Shapefile '{borough_shapefile}' does not exist.")
    exit(1)

# Load the Montreal borough shapefile
boroughs = gpd.read_file(borough_shapefile)

# Load EV charging station data
ev_stations_file = 'filtered_ev_chargers.csv'
if not os.path.exists(ev_stations_file):
    print(f"Error: CSV file '{ev_stations_file}' does not exist.")
    exit(1)

# Read the EV charging stations data
ev_stations = pd.read_csv(ev_stations_file)

# Ensure 'Longitude' and 'Latitude' columns are present
if 'Longitude' not in ev_stations.columns or 'Latitude' not in ev_stations.columns:
    print("Error: 'Longitude' and 'Latitude' columns are missing in the EV chargers file.")
    exit(1)

# Convert EV charging stations to GeoDataFrame with Point geometry
ev_stations['geometry'] = ev_stations.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)
ev_gdf = gpd.GeoDataFrame(ev_stations, geometry='geometry')

# Set the coordinate reference system (CRS) for both datasets (same CRS for spatial join)
ev_gdf = ev_gdf.set_crs('EPSG:4326')

# Transform the boroughs CRS to EPSG:4326
boroughs = boroughs.to_crs('EPSG:4326')

# Perform a spatial join to assign EV stations to boroughs
ev_with_boroughs = gpd.sjoin(ev_gdf, boroughs, how="left", predicate='within')

# Load air quality data
air_quality_file = 'filtered_rqsa_indice-qualite-air-station.csv'
if not os.path.exists(air_quality_file):
    print(f"Error: CSV file '{air_quality_file}' does not exist.")
    exit(1)

# Read the air quality data
air_quality = pd.read_csv(air_quality_file)

# Ensure 'Longitude' and 'Latitude' columns are present
if 'Longitude' not in air_quality.columns or 'Latitude' not in air_quality.columns:
    print("Error: 'Longitude' and 'Latitude' columns are missing in the air quality file.")
    exit(1)

# Convert air quality data to GeoDataFrame with Point geometry
air_quality['geometry'] = air_quality.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)
air_quality_gdf = gpd.GeoDataFrame(air_quality, geometry='geometry')

# Ensure CRS alignment for air quality data
air_quality_gdf = air_quality_gdf.set_crs('EPSG:4326', allow_override=True)

# Perform the spatial join to assign air quality measurements to boroughs
air_quality_with_boroughs = gpd.sjoin(air_quality_gdf, boroughs, how="left", predicate='within')

# Check results
# Update the column name for the boroughs after spatial join
# Assuming 'NOM' is the borough column in the spatial join result
print(ev_with_boroughs[['geometry', 'NOM']])  # EV stations with borough names
print(air_quality_with_boroughs[['geometry', 'Air Quality', 'NOM']])  # Air quality with borough names

# Optionally, save the results to CSV
ev_with_boroughs.to_csv('ev_stations_with_boroughs.csv', index=False)
air_quality_with_boroughs.to_csv('air_quality_with_boroughs.csv', index=False)
