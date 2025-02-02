from flask import Flask, jsonify, request

import pandas as pd
import numpy as np
import csv
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



# Sample Python variables
# Total number of charging stations in mtl
def calculate_total_charging_stations(charging_stations_file):
    total = 0

    # Open the file and read it
    with open(charging_stations_file, mode="r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header

        # Count the number of charging stations
        for row in csv_reader:
            total+=1

    return total
# Average air quality index in mtl
def calculate_total_average_air_quality(air_quality_file):
    total = 0
    count = 0

    # Open the file and read it
    with open(air_quality_file, mode="r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header

        # Sum the air quality index
        for row in csv_reader:
            if len(row) > 1 and row[2].strip():
                total += float(row[2])
                count += 1

    # Calculate the average (avoid division by zero)
    average = total / count if count > 0 else None
    return average

# Number of records for air quality in mtl
def calculate_total_records(air_quality_file):
    count = 0

    # Open the file and read it
    with open(air_quality_file, mode="r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header

        # Count the number of records
        for row in csv_reader:
            count += 1

    return count

# Number of neighbourhood analyzed
def calculate_total_neighbourhoods(neighbourhood_file):
    count = 0

    # Open the file and read it
    with open(neighbourhood_file, mode="r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header

        # Count the number of neighbourhoods
        for row in csv_reader:
            count += 1

    return (count-1)

data = {
    "chargingStations": calculate_total_charging_stations("/Users/thilanthiduong/Documents/CS-year 2/Winter 2025/comp 345/conuhacksIV/flask_server/input files/bornes-recharge-publiques.csv"), 
    "AvgAirQuality": calculate_total_average_air_quality("/Users/thilanthiduong/Documents/CS-year 2/Winter 2025/comp 345/conuhacksIV/flask_server/input files/rsqa-indice-qualite-air.csv"), 
    "NumRecords": calculate_total_records("/Users/thilanthiduong/Documents/CS-year 2/Winter 2025/comp 345/conuhacksIV/flask_server/input files/rsqa-indice-qualite-air.csv"), 
    "NumNeighbourhoods": calculate_total_neighbourhoods("/Users/thilanthiduong/Documents/CS-year 2/Winter 2025/comp 345/conuhacksIV/flask_server/output files/average_air_filtered_with_borough.csv")
    }

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data)

@app.route('/region-info', methods=['GET'])
def get_region_info():
    try:
        # Open and load the JSON file
        with open('/Users/thilanthiduong/Documents/CS-year 2/Winter 2025/comp 345/conuhacksIV/flask_server/output files/summary.json', 'r') as file:
            region_data = json.load(file)
        return jsonify(region_data)
    except Exception as e:
        # If there's an error reading the file, return an error message.
        return jsonify({"error": str(e)}), 500
    
EV_FILE = "/Users/thilanthiduong/Documents/CS-year 2/Winter 2025/comp 345/conuhacksIV/flask_server/output files/average_ev_with_boroughs.csv"
AIR_QUALITY_FILE = "/Users/thilanthiduong/Documents/CS-year 2/Winter 2025/comp 345/conuhacksIV/flask_server/output files/average_air_filtered_with_borough.csv"

def normalize_name(name):
    """Normalize neighborhood names by replacing dash variations."""
    return str(name).replace("\u2010", "-").replace("\u2013", "-").replace("\u2212", "-")

def calculate_pearson(x, y):
    """Compute Pearson Correlation Coefficient."""
    return np.corrcoef(x, y)[0, 1]

@app.route("/api/graph-data", methods=["GET"])
def get_graph_data():
    # Load CSV files
    ev_data = pd.read_csv(EV_FILE)
    air_quality_data = pd.read_csv(AIR_QUALITY_FILE)

    # Normalize neighborhood names
    ev_data["Neighborhood"] = ev_data["Neighborhood"].apply(normalize_name)
    air_quality_data["Neighborhood"] = air_quality_data["Neighborhood"].apply(normalize_name)

    # Merge datasets
    merged_data = pd.merge(ev_data, air_quality_data, on="Neighborhood", how="inner")

    # Select x and y values for Pearson correlation
    x = merged_data["Number of EV Charging Stations"]
    y = merged_data["AVERAGE INDEX"]

    # Calculate Pearson correlation
    corr_coefficient = calculate_pearson(x, y)

    # Prepare response
    response = {
        "data": merged_data.to_dict(orient="records"),
        "correlation": corr_coefficient
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5004, debug=True)
