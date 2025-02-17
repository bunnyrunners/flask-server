from flask import Flask, request, jsonify
import subprocess
import os
import signal

app = Flask(__name__)

@app.route("/")  # This is the crucial addition!
def index():
    return "Welcome niggas!"  # Or any message you want

@app.route("/toggle_script", methods=["POST"])
def toggle_script():
    try:
        if os.path.exists("airtable_sender.run"):
            with open("airtable_sender.stop", "w") as f:
                f.write("")
            return jsonify({"message": "Airtable sender script stopping."}), 200
        else:
            with open("airtable_sender.run", "w") as f:
                f.write("")
            try:
                os.remove("airtable_sender.stop")
            except FileNotFoundError:
                pass
            subprocess.Popen(["python", "airtable_sender.py"])
            return jsonify({"message": "Airtable sender script started."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
