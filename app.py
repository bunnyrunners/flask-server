from flask import Flask, request, jsonify
import subprocess
import os
import signal
import psutil #Import psutil

app = Flask(__name__)

def is_process_running(process_name): #Checks if the process is running
    for proc in psutil.process_iter(['name']):
        if proc.info()['name'] == process_name:
            return True
    return False

@app.route("/toggle_script", methods=["POST"])
def toggle_script():
    try:
        if os.path.exists("airtable_sender.run"):  # Check if the script *might* be running
            try:
                os.remove("airtable_sender.stop")  # Signal the script to stop
            except FileNotFoundError:
                pass  # It's okay if the file doesn't exist

            return jsonify({"message": "Airtable sender script stopping."}), 200

        else:  # Correct indentation here
            try:
                os.remove("airtable_sender.stop")  # Remove the stop signal file if it exists
            except FileNotFoundError:
                pass
            with open("airtable_sender.run", "w") as f:  # Create the file to start
                f.write("")
            if not is_process_running("python"): #Check if the process is already running. If it isn't, run it.
                subprocess.Popen(["python", "airtable_sender.py"])  # Start the process
            return jsonify({"message": "Airtable sender script started."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
