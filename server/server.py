from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# List of Raspberry Pi device URLs
raspberry_pis = [
    "http://localhost:5001/api/status",
    "http://localhost:5002/api/status",
    "http://localhost:5003/api/status",
]

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/status', methods=['GET'])
def check_status():
    statuses = {}
    for pi_url in raspberry_pis:
        pi_name = pi_url.split("//")[1]  # Extracting a name based on the URL
        try:
            response = requests.get(pi_url, timeout=5)
            if response.status_code == 200:
                statuses[pi_name] = "Online"
            else:
                statuses[pi_name] = "Offline"
        except requests.exceptions.RequestException:
            statuses[pi_name] = "Offline"
    return jsonify(statuses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
