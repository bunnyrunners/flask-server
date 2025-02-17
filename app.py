from flask import Flask, request, jsonify
import subprocess
import os
import signal

app = Flask(__name__)

# ... (other Flask routes)

@app.route("/toggle_script", methods=["POST"])
def toggle_script():
    try:
        if os.path.exists("airtable_sender.run"):  # Check if the script is already running
            with open("airtable_sender.stop", "w") as f: #Create the stop signal file
                f.write("")
            return jsonify({"message": "Airtable sender script stopping."}), 200 #Inform the user that the script is stopping
        else:
            with open("airtable_sender.run", "w") as f:  # Start the script (create the file)
                f.write("")
            try:
                os.remove("airtable_sender.stop") #Remove the stop signal file if it exists
            except FileNotFoundError:
                pass
            subprocess.Popen(["python", "airtable_sender.py"])
            return jsonify({"message": "Airtable sender script started."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
