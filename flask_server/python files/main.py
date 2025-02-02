import csv
import os

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
        next(csv_reader)

        for row in csv_reader:
            if (len(row)==5 and row[0]!= '' and row[2]!=''):
                dataAirStation.append(row)

        # Assemble the values per station
        grouped_data = {}
        for row in dataAirStation:
            station = row[0]
            index = row[2]

            if station not in grouped_data:
                grouped_data[station] = []
            
            grouped_data[station].append(index)

        # Calculate the average air quality per station
        average_value = {}

        for station, index in grouped_data.items():
            average_value[station] = sum(index) / len(index)

    # Open the station file to retrieve the coordinates 
    with open(air_input_station, mode = 'r') as file:
        csv_reader = csv.reader
        next(csv_reader)

        for row in csv_reader:
            for station in average_value:
                if (row[0] == station):
                    latitude = row[6]
                    longitude = row[7]
                    average_value[station].append(latitude + longitude)

    # Write the new data to a new csv file (data should have station, avg index, latitude, longitude)
    with open(air_filtered, mode='w') as file:
        csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in average_value:
            csv_writer.writerow(row)
    #---------------------------------------------------------
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
        csv_writer.writerow(["Arrondissement", "Number of EV Charging Stations"])
        for neighborhood, count in station_counts.items():
            csv_writer.writerow([neighborhood,count])
    return

# Method to calculate the average air quality per neighborhood
def calculate_average_air_quality_per_neighborhood(input, output):
    data = []
    # Open the file and read it
    with open(input, mode='r') as file:
        csv_reader = csv.reader(file)
    
        next(csv_reader) # Skip the header
        
        # Append each row to the data list
        for row in csv_reader:
                data.append(row)

        # Group the data by neighborhood
        grouped_data = {}

        for row in data:
            name = row[6]
            index = float (row[2])

            if name not in grouped_data:
                grouped_data[name] = []
            
            grouped_data[name].append(index)
        
        # Calculate the average air quality per neighborhood
        average_value = {}

        for name, index in grouped_data.items():
            average_value[name] = sum(index) / len(index)

    # Write the average data to a new csv file
    with open(output, mode='w') as file:
        csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(["Neighborhood", "Average Air Quality Index"])
        
        for name, index in average_value.items():
            csv_writer.writerow([name, average_value[name]])

    return

station_with_neighborhood = "flask_server/output files/ev_within_bourough.csv"

output_dir = "flask_server/output files/"
os.makedirs(output_dir, exist_ok=True)
station_with_neighborhood_averaged = os.path.join(output_dir, "average_ev_with_boroughs.csv")

count_stations_per_neighborhood(station_with_neighborhood, station_with_neighborhood_averaged)


air_filtered_with_neighborhood = "flask_server/output files/air_quality_within_bourough.csv"
output_dir = "flask_server/output files/"
os.makedirs(output_dir, exist_ok=True)
air_filtered_with_neighborhood_averaged = os.path.join(output_dir, "average_air_filtered_with_borough.csv")
calculate_average_air_quality_per_neighborhood(air_filtered_with_neighborhood, air_filtered_with_neighborhood_averaged)


