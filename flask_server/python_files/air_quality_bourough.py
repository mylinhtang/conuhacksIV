import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import os

# Load the Montreal borough shapefile
borough_shapefile = 'flask_server/agglomeration/limites-administratives-agglomeration-nad83.shp'
try:
    boroughs = gpd.read_file(borough_shapefile)
    print("Shapefile loaded successfully!")
except Exception as e:
    print(f"Error reading shapefile: {e}")
    exit(1)

#load air quality data 
air_quality_file = 'flask_server/output files/filtered_air_quality.csv'
try:
    air_quality = pd.read_csv(air_quality_file)
    print("Air quality data loaded successfully!")
    print(air_quality.head())  # Debug: Display the first few rows to ensure it's loaded properly
except FileNotFoundError:
    print(f"Error: File '{air_quality_file}' not found.")
    exit(1)
except Exception as e:
    print(f"Error reading Air quality station data: {e}")
    exit(1)

# Ensure the file contains the expected columns
if 'LONGITUDE' not in air_quality.columns or 'LATITUDE' not in air_quality.columns:
    print("Error: Air quality station data must contain 'longitude' and 'latitude' columns.")
    exit(1)

# Convert EV charging stations to GeoDataFrame with Point geometry
try:
    air_quality['geometry'] = air_quality.apply(
        lambda row: Point(row['LONGITUDE'], row['LATITUDE']), axis=1
    )
    aq_gdf = gpd.GeoDataFrame(air_quality, geometry='geometry')
    aq_gdf = aq_gdf.set_crs('EPSG:4326')  # Set CRS to WGS84
    print("Air quality successfully converted to GeoDataFrame!")
except Exception as e:
    print(f"Error creating GeoDataFrame for Air quality: {e}")
    exit(1)

# Transform the boroughs CRS to EPSG:4326
try:
    boroughs = boroughs.to_crs('EPSG:4326')
    print("Boroughs CRS transformed to EPSG:4326 successfully!")
except Exception as e:
    print(f"Error transforming CRS for boroughs: {e}")
    exit(1)

# Perform a spatial join to assign Air quality to boroughs
try:
    ev_with_boroughs = gpd.sjoin(aq_gdf, boroughs, how="left", predicate='within')
    print("Spatial join completed successfully!")
except Exception as e:
    print(f"Error performing spatial join for Air quality: {e}")
    exit(1)

# Save the results to CSV
try:
    output_dir = "flask_server/output files/"
    os.makedirs(output_dir, exist_ok=True)
    air_quality_within_bourough = os.path.join(output_dir, "average_air_with_borough.csv")
    ev_with_boroughs.to_csv(air_quality_within_bourough, index=False)
    print("Results saved successfully to 'average_air_with_borough.csv'!")
except Exception as e:
    print(f"Error saving Air quality results to CSV: {e}")
    exit(1)