import time
import requests
import os
import signal

RUNNING_STATUS_FILE = "airtable_sender.run"
STOP_SIGNAL_FILE = "airtable_sender.stop"
url = "https://hooks.airtable.com/workflows/v1/genericWebhook/appTNX6MFpk1UVS4t/wflGCOMfVRUN3LGFJ/wtrqXE99SxadiBekS"  # Define url here

def send_request():
    try:
        print("[INFO] Preparing to send POST request...")
        payload = {"trigger": "true"}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        print("[INFO] Sending POST request...")
        response = requests.post(url, data=payload, headers=headers)  # Use the defined url
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


def signal_handler(sig, frame):
    print('You pressed Ctrl+C or the process was killed!')
    try:
        os.remove(RUNNING_STATUS_FILE)
        print("[INFO] Cleaned up running status file.")
    except FileNotFoundError:
        pass
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

wait = 120  # Define wait here (or earlier)

while True:
    if os.path.exists(RUNNING_STATUS_FILE) and not os.path.exists(STOP_SIGNAL_FILE):
        if not send_request():
            break
        print(f"[INFO] Waiting {wait}s before next request...")
        for i in range(wait, 0, -1):
            print(f"[INFO] {i}s remaining...")
            time.sleep(1)
    else:
        print("[INFO] Script is paused. Waiting for start signal or stop signal...")
        time.sleep(10)
