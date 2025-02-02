import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point

# Load the Montreal borough shapefile
borough_shapefile = 'flask_server/agglomeration/limites-administratives-agglomeration-nad83.shp'

try:
    boroughs = gpd.read_file(borough_shapefile)
    print("Shapefile loaded successfully!")
except Exception as e:
    print(f"Error loading shapefile: {e}")
    exit(1)

# Load EV charging station data
ev_stations_file = 'flask_server/output files/filtered_ev_chargers.csv'

try:
    ev_stations = pd.read_csv(ev_stations_file)
    print("EV charging station data loaded successfully!")
    print(ev_stations.head())
except Exception as e:
    print(f"Error loading EV charging station data: {e}")
    exit(1)

# Convert EV charging stations to GeoDataFrame with Point geometry
try:
    ev_stations['geometry'] = ev_stations.apply(lambda row: Point(row['LONGITUDE'], row['LATITUDE']), axis=1)
    ev_gdf = gpd.GeoDataFrame(ev_stations, geometry='geometry')
    ev_gdf = ev_gdf.set_crs('EPSG:4326')  # Set CRS to WGS84
    print("EV charging stations converted to GeoDataFrame successfully!")
except Exception as e:
    print(f"Error creating GeoDataFrame for EV charging stations: {e}")
    exit(1)

# Ensure boroughs CRS matches EV data CRS
try:
    boroughs = boroughs.to_crs('EPSG:4326')
    print("Boroughs CRS transformed to EPSG:4326 successfully!")
except Exception as e:
    print(f"Error transforming boroughs CRS: {e}")
    exit(1)

# Plotting the data
try:
    fig, ax = plt.subplots(figsize=(10, 10))

    # Plot the boroughs
    boroughs.plot(ax=ax, color='lightgray', edgecolor='black', alpha=0.7)

    # Plot EV charging stations
    ev_gdf.plot(ax=ax, color='red', marker='o', label='EV Stations', alpha=0.8)

    # Customize plot
    plt.title('Montreal EV Charging Stations and Boroughs', fontsize=16)
    plt.legend()
    plt.show()
    print("Plot displayed successfully!")
except Exception as e:
    print(f"Error during plotting: {e}")
    exit(1)
