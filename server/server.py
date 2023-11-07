import io
from flask import Flask, jsonify, render_template, send_file
import requests
from io import BytesIO

app = Flask(__name__)

# A list containing the URLs of the Raspberry Pi devices
raspberry_pis = [
    "http://192.168.0.105:5001",
    "http://localhost:5002",
    "http://localhost:5003",
]

@app.route('/')
def dashboard():
    # Render the dashboard page
    return render_template('dashboard.html')

# Function to fetch data from Raspberry Pis. Abstracting this into a separate function avoids code repetition.
def fetch_from_pi(device_id, endpoint):
    try:
        # Validate device_id
        if 0 < device_id <= len(raspberry_pis):
            pi_url = raspberry_pis[device_id-1]
            response = requests.get(f"{pi_url}/api/{endpoint}", timeout=5)
            data = response.json()
            data['client_id'] = f"Client {device_id}"
        else:
            data = {"error": "Invalid device_id"}
    except requests.exceptions.RequestException:
        data = {"client_id": f"Client {device_id}", "status": "Offline"}
    return jsonify(data)

@app.route('/api/health/<int:device_id>', methods=['GET'])
def get_health(device_id):
    # Fetch health data from the Raspberry Pi
    return fetch_from_pi(device_id, 'health')

@app.route('/api/network_settings/<int:device_id>', methods=['GET'])
def get_network_settings(device_id):
    # Fetch network settings from the Raspberry Pi
    return fetch_from_pi(device_id, 'network_settings')

@app.route('/api/ntp_check/<int:device_id>', methods=['GET'])
def ntp_check(device_id):
    # Fetch NTP check data from the Raspberry Pi
    return fetch_from_pi(device_id, 'ntp_check')

@app.route('/api/camera_check/<int:device_id>', methods=['GET'])
def camera_check(device_id):
    # Fetch camera data from the Raspberry Pi
    return fetch_from_pi(device_id, 'camera_check')

@app.route('/api/take_photo/<int:device_id>', methods=['GET'])
def take_photo(device_id):
    try:
        pi_url = raspberry_pis[device_id-1]
        response = requests.get(f"{pi_url}/api/take_photo", stream=True)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Return the content as a response with the correct content-type
            return send_file(
                io.BytesIO(response.content),
                mimetype='image/jpeg',  # Adjust the mimetype according to the actual image format
                as_attachment=True,
                download_name="captured_image.jpg"
            )

        else:
            return jsonify({"error": "Failed to capture photo, invalid status code."})

    except requests.exceptions.RequestException:
        return jsonify({"error": "Failed to capture photo."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)