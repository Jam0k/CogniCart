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

@app.route('/api/health', methods=['GET'])
def get_health():
    health_data = {}
    
    for i, pi_url in enumerate(raspberry_pis, start=1):
        try:
            response = requests.get(f"{pi_url}/api/health", timeout=5)
            health_data[f"Client {i}"] = response.json()
        except requests.exceptions.RequestException:
            health_data[f"Client {i}"] = {"status": "Offline"}
    
    return jsonify(health_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
