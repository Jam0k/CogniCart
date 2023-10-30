from flask import Flask, jsonify
import psutil
import socket
import subprocess

app = Flask(__name__)

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')
        
        return jsonify({
            "status": "Online",
            "cpu_usage": f"{cpu_usage}%",
            "memory_usage": f"{memory_info.percent}%",
            "disk_usage": f"{disk_info.percent}%"
        })
    except Exception:
        return jsonify({"status": "Error fetching health data"})
    
@app.route('/api/network_settings', methods=['GET'])
def network_settings():
    try:
        # Getting hostname
        hostname = socket.gethostname()

        # Getting IP Address
        ip_address = socket.gethostbyname(hostname)

        # Getting MAC Address (You might need to adjust 'eth0' based on your device)
        try:
            mac_address = ':'.join(['{:02x}'.format((ord(c))) for c in open('/sys/class/net/eth0/address').read()])
        except:
            mac_address = "N/A"

        # Getting WiFi SSID
        try:
            ssid = subprocess.check_output(["iwgetid", "-r"]).strip().decode()
        except:
            ssid = "N/A"

        return jsonify({
            "status": "Online",
            "hostname": hostname,
            "ip_address": ip_address,
            "mac_address": mac_address,
            "wifi_ssid": ssid
        })
    except Exception as e:
        return jsonify({"status": f"Error fetching network data: {str(e)}"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
