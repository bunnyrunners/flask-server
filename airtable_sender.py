import time
import requests
import os
import signal

RUNNING_STATUS_FILE = "airtable_sender.run"
STOP_SIGNAL_FILE = "airtable_sender.stop"

def send_request():
    # ... (your send_request function - no changes needed)
    try:
        print("[INFO] Preparing to send POST request...")
        payload = {"trigger": "true"}  # Example payload
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        print("[INFO] Sending POST request...")
        response = requests.post(url, data=payload, headers=headers)
        print("[INFO] Waiting for response...")
        print(f"[INFO] Response received: {response.text}")

        if response.status_code != 200:
            print(f"[ERROR] Request failed with status code {response.status_code}. Stopping automation.")
            return False
        print("[INFO] Request successful.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        return False


def signal_handler(sig, frame):  # Correctly defined at the top level
    print('You pressed Ctrl+C or the process was killed!')
    try:
        os.remove(RUNNING_STATUS_FILE)
        print("[INFO] Cleaned up running status file.")
    except FileNotFoundError:
        pass
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:  # Correct indentation here
    if os.path.exists(RUNNING_STATUS_FILE) and not os.path.exists(STOP_SIGNAL_FILE):
        if not send_request():
            break  # Exit loop if sending fails
        print(f"[INFO] Waiting {wait}s before next request...")
        for i in range(wait, 0, -1):  # Correct indentation here
            print(f"[INFO] {i}s remaining...")  # Correct indentation here
            time.sleep(1)  # Correct indentation here
    else:
        print("[INFO] Script is paused. Waiting for start signal or stop signal...")
        time.sleep(10)  # Check every 10 seconds for the file  # Correct indentation here
