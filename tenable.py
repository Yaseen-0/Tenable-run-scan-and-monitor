import requests
import time

# Configure Tenable.sc API
BASE_URL = "https://10.9.9.169/rest"  # Replace with your Tenable.sc IP/domain
ACCESS_KEY = "5b5ff70ccb8241c79f84a9363f3fc551"  # Replace with the API access key
SECRET_KEY = "b5c2f7c68ea9468cbe1f8c9dda4f8c74"  # Replace with the API secret key
VERIFY_SSL = False  # Change to True if using SSL certificates

# Disable SSL warnings if VERIFY_SSL=False
if not VERIFY_SSL:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Predefined scan ID and scan result ID
scan_id = "9"  # Replace with your scan ID
scan_result_id = "55"  # Replace with your scan result ID

# Function to authenticate and get user details
def authenticate_to_tenable():
    url = f"{BASE_URL}/currentUser"
    headers = {
        "x-apikey": f"accesskey={ACCESS_KEY}; secretkey={SECRET_KEY}"
    }

    try:
        response = requests.get(url, headers=headers, verify=VERIFY_SSL)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print("Authentication successful!")
        return response.json()  # Return the JSON response
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Function to start a scan by ID
def start_scan(scan_id):
    url = f"{BASE_URL}/scan/{scan_id}/launch"
    headers = {
        "x-apikey": f"accesskey={ACCESS_KEY}; secretkey={SECRET_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers, verify=VERIFY_SSL)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(f"Scan {scan_id} started successfully!")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Function to monitor the scan's progress using scan result ID
def monitor_scan_result(result_id):
    url = f"{BASE_URL}/scanResult/{result_id}"
    headers = {
        "x-apikey": f"accesskey={ACCESS_KEY}; secretkey={SECRET_KEY}"
    }

    try:
        while True:
            response = requests.get(url, headers=headers, verify=VERIFY_SSL)
            response.raise_for_status()  # Raise an exception for HTTP errors
            status = response.json()["response"]["status"]
            print(f"Scan status: {status}")

            if status == "Completed":
                print("Scan completed successfully!")
                return True
            elif status == "Error":
                print("Scan encountered an error.")
                return False
            else:
                print("Scan is still running. Waiting...")
                time.sleep(10)  # Wait for 10 seconds before checking again
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Main workflow
if __name__ == "__main__":
    user_details = authenticate_to_tenable()
    if user_details:
        print("User Details:")
        print(user_details)

        # Start the scan if required
        start_scan(scan_id)

        # Monitor the scan using the predefined scan result ID
        if monitor_scan_result(scan_result_id):
            print(f"Monitoring for Scan Result ID {scan_result_id} completed.")
