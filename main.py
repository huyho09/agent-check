import requests
import csv
import os
from datetime import datetime
import time

# --- Configuration ---
API_URL = "https://cx.bosch-so.com/rexroth-chat-DC-ready"
API_NAME = "GP_Bosch_Rexroth_Chat_DC_VAG"
CSV_FILE = "agent_availability_log.csv"
CHECK_INTERVAL_SECONDS = 900  # 15 minutes

def check_agent_availability():
    """
    Checks the API for available agents and logs the result to a CSV file.
    """
    print(f"[{datetime.now()}] Running agent availability check...")

    try:
        # --- 1. Make the API Call ---
        response = requests.get(API_URL, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # --- 2. Parse the Response ---
        data = response.json()
        available_agents = data.get(API_NAME, 0) # Default to 0 if key is not found

        print(f"[{datetime.now()}] Successfully fetched data. Available agents: {available_agents}")

        # --- 3. Log to CSV ---
        log_to_csv(API_NAME, available_agents)

    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] Error: Could not connect to the API. {e}")
        log_to_csv(API_NAME, "Connection Error")
    except ValueError as e: # Catches JSON decoding errors
        print(f"[{datetime.now()}] Error: Could not parse the API response. {e}")
        log_to_csv(API_NAME, "Invalid JSON Response")
    except Exception as e:
        print(f"[{datetime.now()}] An unexpected error occurred: {e}")
        log_to_csv(API_NAME, "Unknown Error")


def log_to_csv(api_name, agent_count):
    """
    Appends a new record to the CSV log file.
    Creates the file and adds a header if it doesn't exist.
    """
    # --- Check if file exists to write header ---
    file_exists = os.path.isfile(CSV_FILE)

    try:
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as csv_file:
            # --- Define CSV columns ---
            fieldnames = ['Timestamp', 'APIName', 'AvailableAgents']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # --- Write header if file is new ---
            if not file_exists:
                writer.writeheader()
                print(f"[{datetime.now()}] Created new log file: {CSV_FILE}")

            # --- Write the data row ---
            writer.writerow({
                'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'APIName': api_name,
                'AvailableAgents': agent_count
            })
    except IOError as e:
        print(f"[{datetime.now()}] Error: Could not write to CSV file. {e}")


if __name__ == "__main__":
    # This block allows the script to be run directly.
    # For the GitHub Action, we will call the function directly.
    # For local testing, you can uncomment the loop.
    
    # --- For GitHub Actions, we just need one run ---
    check_agent_availability()

    # --- For local continuous running, uncomment the following lines ---
    # print("Starting continuous monitoring. Press Ctrl+C to stop.")
    # while True:
    #     check_agent_availability()
    #     print(f"Sleeping for {CHECK_INTERVAL_SECONDS / 60} minutes...")
    #     time.sleep(CHECK_INTERVAL_SECONDS)

