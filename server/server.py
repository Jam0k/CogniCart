from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/send', methods=['POST'])
def send_command():
    command = request.get_json().get('command')
    
    # URL of the Raspberry Pi endpoint that will receive the command
    raspberry_pi_url = "http://localhost:5001/receive"
    
    # Forwarding the command to the Raspberry Pi
    response = requests.post(raspberry_pi_url, json={"command": command})
    
    # Check if the request was successful
    if response.status_code == 200:
        return jsonify({"message": "Command sent to Raspberry Pi", "pi_response": response.json()})
    else:
        return jsonify({"message": "Failed to send command to Raspberry Pi", "pi_response": response.json()}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
