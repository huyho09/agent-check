import requests
import csv
import os
from datetime import datetime
import time
import pytz  # Import the pytz library

# --- Configuration ---
API_URL = "https://cx.bosch-so.com/rexroth-chat-DC-ready"
API_NAME = "GP_Bosch_Rexroth_Chat_DC_VAG"
# Updated to use result.csv as requested
CSV_FILE = "result.csv" 
CHECK_INTERVAL_SECONDS = 900  # 15 minutes

def get_cet_time():
    """
    Gets the current time in the CET timezone.
    """
    cet_timezone = pytz.timezone('CET')
    return datetime.now(cet_timezone)

def check_agent_availability():
    """
    Checks the API for available agents and logs the result to a CSV file.
    """
    current_time_str = get_cet_time().strftime('%Y-%m-%d %H:%M:%S %Z')
    print(f"[{current_time_str}] Running agent availability check...")

    try:
        # --- 1. Make the API Call ---
        # Set a timeout to prevent the script from hanging indefinitely.
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # --- 2. Parse the Response ---
        # We assume the response is JSON.
        data = response.json()
        available_agents = data.get(API_NAME, 0) # Default to 0 if the key is not found

        print(f"[{current_time_str}] Successfully fetched data. Available agents: {available_agents}")

        # --- 3. Log to CSV ---
        log_to_csv(API_NAME, available_agents)

    except requests.exceptions.RequestException as e:
        print(f"[{current_time_str}] Error: Could not connect to the API. {e}")
        log_to_csv(API_NAME, "Connection Error")
    except ValueError as e: # Catches JSON decoding errors
        print(f"[{current_time_str}] Error: Could not parse the API response. {e}")
        log_to_csv(API_NAME, "Invalid JSON Response")
    except Exception as e:
        print(f"[{current_time_str}] An unexpected error occurred: {e}")
        log_to_csv(API_NAME, "Unknown Error")


def log_to_csv(api_name, agent_count):
    """
    Appends a new record to the CSV log file.
    Creates the file and adds a header if it doesn't exist.
    """
    # Check if the CSV file already exists to determine if we need to write the header.
    file_exists = os.path.isfile(CSV_FILE)
    current_time = get_cet_time()

    try:
        # Open the file in 'append' mode. This creates the file if it doesn't exist.
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as csv_file:
            # Define the column names for the CSV file.
            fieldnames = ['Timestamp', 'APIName', 'AvailableAgents']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # If the file did not exist before opening, write the header row.
            if not file_exists:
                writer.writeheader()
                print(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}] Created new log file: {CSV_FILE}")

            # Write the actual data row.
            writer.writerow({
                'Timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
                'APIName': api_name,
                'AvailableAgents': agent_count
            })
    except IOError as e:
        print(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}] Error: Could not write to CSV file. {e}")


if __name__ == "__main__":
    # This main execution block is what gets run by the GitHub Action.
    # It performs a single check and logs the result.
    check_agent_availability()