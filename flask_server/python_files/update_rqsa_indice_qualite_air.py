import os
import requests
import pandas as pd
import csv

def fetch_rqsa_indice_qualite_air_data():
    url = 'https://donnees.montreal.ca/api/3/action/datastore_search'
    params = {
        'resource_id': 'a25fdea2-7e86-42ac-8301-ca77db3ff17e',
        'q': '',  # Empty query to fetch everything
        'limit': 1000,  # Adjust the number of records to fetch
        'offset': 0  # Start from the first record
    }
    
    # File path and directory setup
    file_path = './flask_server/input files/rqsa-indice-qualite-air.csv'
    directory = os.path.dirname(file_path)
    all_records = []  # List to store all the records

    try:
        # Ensure the output directory exists
        if directory:  # Check if directory is not empty (handles files directly in the current directory)
            os.makedirs(directory, exist_ok=True)

        while True:
            print(f"Sending API request with offset {params['offset']}...")
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise exception for HTTP errors

            print(f"API Request Successful! Status Code: {response.status_code}")

            # Parse the response JSON
            data = response.json()

            # Get records
            records = data.get('result', {}).get('records', [])
            print(f"Found {len(records)} records.")

            if records:
                all_records.extend(records)
            else:
                break  # No more records to fetch

            # Update offset for the next batch of records
            params['offset'] += params['limit']

        if all_records:
            print(f"Total records fetched: {len(all_records)}")

            # Convert records to DataFrame
            df = pd.DataFrame(all_records)

            # Print a sample of the data for preview
            print("Sample Data:")
            print(df.head())

            # Drop _id column if it exists
            if '_id' in df.columns:
                df = df.drop('_id', axis=1)

            # Save the updated data to a CSV file
            df.to_csv(
                file_path,
                index=False,
                quoting=csv.QUOTE_MINIMAL,  # Quotes only when necessary
                quotechar='"',  # Use double quotes for fields
                escapechar='\\',  # Escape special characters if necessary
                header=True
            )
            print(f"Data saved to '{file_path}'!")
            # Display how the data is written to the CSV
            print("\nSample Data (as written in CSV):")
            print(df.head().to_csv(index=False, quoting=csv.QUOTE_MINIMAL, quotechar='"', escapechar='\\', header=True))
        else:
            print("No records found in the API response.")

    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
    except OSError as e:
        print(f"Error saving the file: {e}")

# Call the function to fetch the data
fetch_rqsa_indice_qualite_air_data()
