import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Method to read csv files, filter, and store its data in another CSV file (EV chargers)
def read_csv_evChargers(ev_input, ev_filtered):
    data = []
    
    # Open the file and read it
    with open(ev_input, mode='r') as file:
        csv_reader = csv.reader(file)
        
        # Append each row (if it is valid) to the data list
        for row in csv_reader:
            if len(row) == 10 and row[8] != '' and row[9] != '':
                # Only write the longitudes and latitudes (Col 9 and 10)
                data.append(row[8:10])
        
    
    # Write the filtered data to a new csv file
    with open(ev_filtered, mode='w') as file:
        csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            csv_writer.writerow(row)

    return 

#Method to read csv file, filter, and store its data in another csv file (air quality)
def read_csv_airQuality(air_input, air_input_station, air_filtered):
    dataAirStation = []

    # Open the quality air index by station file 
    with open(air_input, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header

        for row in csv_reader:
            if len(row) == 5 and row[0] != '' and row[2] != '':
                dataAirStation.append(row)

    # Assemble the values per station
    grouped_data = {}
    for row in dataAirStation:
        station = row[0]
        index = float(row[2])  # Convert index to float

        if station not in grouped_data:
            grouped_data[station] = []
        
        grouped_data[station].append(index)

    # Calculate the average air quality per station
    average_value = {}
    for station, index_list in grouped_data.items():
        average_value[station] = [sum(index_list) / len(index_list)]  # Store as a list

    # Open the station file to retrieve the coordinates 
    with open(air_input_station, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header

        for row in csv_reader:
            station = row[0]
            if station in average_value:
                latitude = float(row[6])  # Convert to float
                longitude = float(row[7])  # Convert to float
                average_value[station].extend([longitude, latitude])  # Append coords

    # Write the new data to a new CSV file
    with open(air_filtered, mode='w', newline='') as file:
        csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Write header
        csv_writer.writerow(["STATION", "AVERAGE INDEX", "LONGITUDE", "LATITUDE"])

        for station, values in average_value.items():
            csv_writer.writerow([station] + values)  # Write all data

    return  


ev_input = "flask_server/input files/bornes-recharge-publiques.csv"
output_dir = "flask_server/output files/"
os.makedirs(output_dir, exist_ok=True)
ev_filtered = os.path.join(output_dir, "filtered_ev_chargers.csv")

air_input = "flask_server/input files/rsqa-indice-qualite-air.csv"
air_input_station = "flask_server/input files/liste-des-stations-rsqa.csv"
air_filtered = os.path.join(output_dir, "filtered_air_quality.csv")

read_csv_evChargers(ev_input, ev_filtered)
read_csv_airQuality(air_input, air_input_station, air_filtered)

# Method to filter uneccessary columns for avg air quality with boroughs
def filter_air_quality(air_quality_input, air_quality_filtered):
    data = []
    
    # Open the file and read it
    with open(air_quality_input, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        
        # Append each row (if it is valid) to the data list
        for row in csv_reader:
            # Only write the name and avg index (Col 2 and 8)
            data.append([row[8], row[1]])
    
    # Write the filtered data to a new csv file
    with open(air_quality_filtered, mode='w') as file:
        csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["NOM", "AVERAGE INDEX"])
        for row in data:
            csv_writer.writerow(row)

    return

air_quality_input = "flask_server/output files/average_air_with_borough.csv"
output_dir = "flask_server/output files/"
os.makedirs(output_dir, exist_ok=True)
air_quality_filtered = os.path.join(output_dir, "average_air_filtered_with_borough.csv")
filter_air_quality(air_quality_input, air_quality_filtered)

def count_stations_per_neighborhood(stations_input, stations_averaged): 
    station_counts = {} #dictionnary

    #read stations with boroughs
    with open(stations_input, mode="r") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader) #skip header

        #find the neighborhood name
        try: 
            neighborhood_index = header.index("NOM")
        except: 
            print("Error, no \"NOM\" column found in the CSV file")
            return
        
        #count stations per neighborhood
        for row in csv_reader:
            if len(row) > neighborhood_index and row[neighborhood_index].strip(): 
                neighborhood = row[neighborhood_index] #get neighborhood name
                if neighborhood in station_counts:  #check if neighborhood exists in the dictionnary -> +1 count
                    station_counts[neighborhood] += 1
                else: 
                    station_counts[neighborhood] = 1

    #write csv file
    with open(stations_averaged, mode="w") as file: 
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Neighborhood", "Number of EV Charging Stations"])
        for neighborhood, count in station_counts.items():
            csv_writer.writerow([neighborhood,count])
    return


station_with_neighborhood = "flask_server/output files/ev_within_bourough.csv"
output_dir = "flask_server/output files/"
os.makedirs(output_dir, exist_ok=True)
station_with_neighborhood_averaged = os.path.join(output_dir, "average_ev_with_boroughs.csv")

count_stations_per_neighborhood(station_with_neighborhood, station_with_neighborhood_averaged)

#method to calculate the total average air quality in montreal
def calculate_total_average_air_quality(air_quality_file):
    total = 0
    count = 0

    #open the file and read it
    with open(air_quality_file, mode="r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader) #skip header

        #sum the air quality index
        for row in csv_reader:
            if len(row) > 1 and row[2].strip(): 
                total += float(row[2])
                count += 1

    #calculate the average
    average = total / count
    return average

air_quality_filtered = "flask_server/input files/rsqa-indice-qualite-air.csv"
average_air_quality = calculate_total_average_air_quality(air_quality_filtered)
print(f"Total average air quality in Montreal: {average_air_quality}")



# def plot_graph(ev_file, air_quality_file):
#     #load dataset
#     ev_data = pd.read_csv(ev_file)
#     air_quality_data = pd.read_csv(air_quality_file)
#     #keep data of neighborhoods only in air quality data file
#     common_neighborhoods = ev_data[ev_data["Neighborhood"].isin(air_quality_data["Neighborhood"])]
#     merged_data = pd.merge(common_neighborhoods, air_quality_data, on="Neighborhood")

#     # Scatter plot
#     plt.figure(figsize=(8, 5))
#     sns.scatterplot(
#     x=merged_data["Number of EV Charging Stations"], 
#     y=merged_data["Average Air Quality Index"], 
#     hue=merged_data["Neighborhood"], 
#     s=100, palette="viridis"
#     )

#     # Add labels & title
#     plt.xlabel("Number of EV Charging Stations")
#     plt.ylabel("Air Quality Index (Higher = Worse)")
#     plt.title("Correlation Between Air Quality & EV Stations")
#     plt.legend(title="Neighborhood")

#     # Show plot
#     plt.show()

# ev_file = "flask_server/output files/average_ev_with_boroughs.csv"
# air_quality_file = "flask_server/output files/average_air_filtered_with_borough.csv"
# plot_graph(ev_file, air_quality_file)










