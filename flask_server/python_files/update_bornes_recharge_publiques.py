import os
import requests
import pandas as pd
import csv

def fetch_bornes_recharges_publiques_data():
    url = 'https://donnees.montreal.ca/api/3/action/datastore_search'
    params = {
        'resource_id': '98ef3ed6-56ca-4d5e-a213-fd72066b18b5',
        'q': '',  # Empty query to fetch everything
        'limit': 1000,  # Adjust the number of records to fetch
        'offset': 0  # Start from the first record
    }

    # Ensure the output directory exists
    output_file = './flask_server/input files/bornes-recharge-publiques.csv'
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)

    all_records = []  # List to store all the records

    try:
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

            # Drop _id column if it exists
            if '_id' in df.columns:
                df = df.drop('_id', axis=1)

            # Add quotes around every field value except LONGITUDE and LATITUDE
            for col in df.columns:
                if col not in ['LONGITUDE', 'LATITUDE']:
                    df[col] = df[col].apply(lambda x: f'"{x}"' if isinstance(x, str) else x)

            # Save the updated data to a CSV file with quotes around all fields except LONGITUDE and LATITUDE
            df.to_csv(
                output_file,
                index=False,
                quoting=csv.QUOTE_NONE,  # Do not quote fields with commas by default
                quotechar='"',  # Ensure fields are quoted with double quotes
                escapechar='\\',  # Escape special characters if necessary
                header=True
            )
            print(f"Data saved to '{output_file}'!")
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
fetch_bornes_recharges_publiques_data()
