import json
import os
import time
import requests
from datetime import datetime
from collections import defaultdict

# Function to fetch and return data from the given URL
def fetch_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None

# Function to process mask data
def process_mask_data(input_data):
    aggregated_data = defaultdict(lambda: {'masked': 0, 'no mask': 0})
    for entry in input_data:
        date = datetime.strptime(entry['timestamp'], '%a, %d %b %Y %H:%M:%S GMT').date().isoformat()
        if entry['mask_status']:
            aggregated_data[date]['masked'] += 1
        else:
            aggregated_data[date]['no mask'] += 1
    return aggregated_data

# Function to process temperature data
def process_temperature_data(input_data):
    aggregated_data = defaultdict(lambda: {'normal temperature': 0, 'high temperature': 0})
    for entry in input_data:
        date = datetime.strptime(entry['timestamp'], '%a, %d %b %Y %H:%M:%S GMT').date().isoformat()
        if entry['temperature'] > 37:
            aggregated_data[date]['high temperature'] += 1
        else:
            aggregated_data[date]['normal temperature'] += 1
    return aggregated_data

# Function to convert aggregated data to desired format
def convert_to_format(aggregated_data, type1, type2):
    result = []
    for date, counts in aggregated_data.items():
        result.append({"date": date, "value": counts[type1], "type": type1})
        if counts[type2] > 0:
            result.append({"date": date, "value": counts[type2], "type": type2})
    return result

# Function to save the result to a JSON file
def save_to_file(data, folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(file_path, 'w') as output_file:
        json.dump(data, output_file, indent=2)
    print(f"Data successfully saved to {file_path}")

# Main function to handle both mask and temperature data processing
def convert_data_to_jason():
    url = "http://127.0.0.1:5000/entries"
    

    while True:
        input_data = fetch_data(url)
        if input_data:
            # Process and save mask data
            mask_data = process_mask_data(input_data)
            mask_result = convert_to_format(mask_data, "masked", "no mask")
            save_to_file(mask_result, "../cli/src/data", "mask_data.json")

            # Process and save temperature data
            temp_data = process_temperature_data(input_data)
            temp_result = convert_to_format(temp_data, "normal temperature", "high temperature")
            save_to_file(temp_result, "../cli/src/data", "temp_data.json")
        # Wait for 60 second before fetching the data again
        time.sleep(60)
        print("Convert data again...")

