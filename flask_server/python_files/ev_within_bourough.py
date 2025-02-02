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

# Load EV charging station data
ev_stations_file = 'flask_server/output files/filtered_ev_chargers.csv'
try:
    ev_stations = pd.read_csv(ev_stations_file)
    print("EV charging station data loaded successfully!")
    print(ev_stations.head())  # Debug: Display the first few rows to ensure it's loaded properly
except FileNotFoundError:
    print(f"Error: File '{ev_stations_file}' not found.")
    exit(1)
except Exception as e:
    print(f"Error reading EV charging station data: {e}")
    exit(1)

# Ensure the file contains the expected columns
if 'LONGITUDE' not in ev_stations.columns or 'LATITUDE' not in ev_stations.columns:
    print("Error: EV charging station data must contain 'LONGITUDE' and 'LATITUDE' columns.")
    exit(1)

# Convert EV charging stations to GeoDataFrame with Point geometry
try:
    ev_stations['geometry'] = ev_stations.apply(
        lambda row: Point(row['LONGITUDE'], row['LATITUDE']), axis=1
    )
    ev_gdf = gpd.GeoDataFrame(ev_stations, geometry='geometry')
    ev_gdf = ev_gdf.set_crs('EPSG:4326')  # Set CRS to WGS84
    print("EV charging stations successfully converted to GeoDataFrame!")
except Exception as e:
    print(f"Error creating GeoDataFrame for EV charging stations: {e}")
    exit(1)

# Transform the boroughs CRS to EPSG:4326
try:
    boroughs = boroughs.to_crs('EPSG:4326')
    print("Boroughs CRS transformed to EPSG:4326 successfully!")
except Exception as e:
    print(f"Error transforming CRS for boroughs: {e}")
    exit(1)

# Perform a spatial join to assign EV stations to boroughs
try:
    ev_with_boroughs = gpd.sjoin(ev_gdf, boroughs, how="left", predicate='within')
    print("Spatial join completed successfully!")
except Exception as e:
    print(f"Error performing spatial join for EV stations: {e}")
    exit(1)

# Save the results to CSV
try:
    output_dir = "flask_server/output files/"
    os.makedirs(output_dir, exist_ok=True)
    ev_within_bourough = os.path.join(output_dir, "ev_within_bourough.csv")
    ev_with_boroughs.to_csv(ev_within_bourough, index=False)
    print("Results saved successfully to 'ev_within_bourough.csv'!")
except Exception as e:
    print(f"Error saving EV station results to CSV: {e}")
    exit(1)
