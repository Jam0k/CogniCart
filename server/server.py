from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

raspberry_pis = [
    "http://localhost:5001",
    "http://localhost:5002",
    "http://localhost:5003",
]

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/health/<int:device_id>', methods=['GET'])
def get_health(device_id):
    try:
        # Ensure the device_id is valid
        if 0 < device_id <= len(raspberry_pis):
            pi_url = raspberry_pis[device_id-1]
            response = requests.get(f"{pi_url}/api/health", timeout=5)
            health_data = response.json()
            health_data['client_id'] = f"Client {device_id}"
        else:
            health_data = {"error": "Invalid device_id"}
    except requests.exceptions.RequestException:
        health_data = {"client_id": f"Client {device_id}", "status": "Offline"}
    
    return jsonify(health_data)

@app.route('/api/network_settings/<int:device_id>', methods=['GET'])
def get_network_settings(device_id):
    try:
        # Ensure the device_id is valid
        if 0 < device_id <= len(raspberry_pis):
            pi_url = raspberry_pis[device_id-1]
            response = requests.get(f"{pi_url}/api/network_settings", timeout=5)
            network_data = response.json()
            network_data['client_id'] = f"Client {device_id}"
        else:
            network_data = {"error": "Invalid device_id"}
    except requests.exceptions.RequestException:
        network_data = {"client_id": f"Client {device_id}", "status": "Offline"}
    
    return jsonify(network_data)

@app.route('/api/ntp_check/<int:device_id>', methods=['GET'])
def ntp_check(device_id):
    try:
        # Ensure the device_id is valid
        if 0 < device_id <= len(raspberry_pis):
            pi_url = raspberry_pis[device_id-1]
            response = requests.get(f"{pi_url}/api/ntp_check", timeout=5)
            ntp_data = response.json()
            ntp_data['client_id'] = f"Client {device_id}"
        else:
            ntp_data = {"error": "Invalid device_id"}
    except requests.exceptions.RequestException:
        ntp_data = {"client_id": f"Client {device_id}", "status": "Offline"}
    
    return jsonify(ntp_data)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
