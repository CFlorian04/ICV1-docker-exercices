from flask import Flask, jsonify
import os
import json
import requests

app = Flask(__name__)

@app.route('/')
def ping():
    receiver_code = "s2"
    annuaire_HOST = os.environ.get("MEDIATOR_URL", "http://ex3_annuaire:8080")

    # Fetch information from the annuaire
    try:
        annuaire_response = requests.get(annuaire_HOST)
        server_list = json.loads(annuaire_response.text)
        receiver_info = server_list[receiver_code]
        receiver_HOST = receiver_info["host"]
        receiver_PORT = receiver_info["port"]
        print(f"Annuaire, adresse IP {receiver_HOST}, port {receiver_PORT}")

        pong_response = requests.get(f"http://{receiver_HOST}:{receiver_PORT}/pong")
        pong_message = pong_response.json()["message"]
        print(f"Received from Pong server: {pong_message}")

    except requests.RequestException as e:
        print(f"Error connecting to annuaire: {e}")
        return jsonify({"error": "Connection to annuaire failed"}), 500

    # Placeholder response for testing purposes
    return jsonify({"message": "PING"}), 200

if __name__ == "__main__":
    print("Run Server Ping")
    app.run(host='0.0.0.0', port=4567)
