from flask import Flask, jsonify, send_file
import psutil
import socket
import subprocess
from datetime import datetime
from io import BytesIO

app = Flask(__name__)

def fetch_data_from_system(command, error_message="N/A"):
    try:
        return subprocess.check_output(command).strip().decode()
    except:
        return error_message

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
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        mac_address = fetch_data_from_system(["cat", "/sys/class/net/eth0/address"])
        wifi_ssid = fetch_data_from_system(["iwgetid", "-r"])

        return jsonify({
            "status": "Online",
            "hostname": hostname,
            "ip_address": ip_address,
            "mac_address": mac_address,
            "wifi_ssid": wifi_ssid
        })
    except Exception as e:
        return jsonify({"status": f"Error fetching network data: {str(e)}"})

@app.route('/api/ntp_check', methods=['GET'])
def ntp_check_client():
    try:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return jsonify({"status": "Online", "current_ntp_time": current_time})
    except Exception as e:
        return jsonify({"status": "Error fetching system time", "error": str(e)})
    

@app.route('/api/camera_check', methods=['GET'])
def camera_check():
    try:
        # Using subprocess to execute a shell command that checks the camera status
        camera_status = subprocess.check_output(["vcgencmd", "get_camera"]).strip().decode()
        return jsonify({"status": "Online", "camera_status": camera_status})
    except Exception as e:
        return jsonify({"status": f"Error fetching camera data: {str(e)}"})
    
@app.route('/api/take_photo', methods=['GET'])
def take_photo():
    try:
        # Using subprocess to execute the libcamera-still command
        image_stream = BytesIO()
        process = subprocess.Popen(["libcamera-still", "-o", "-"], stdout=subprocess.PIPE)
        out, err = process.communicate()
        image_stream.write(out)
        image_stream.seek(0)
        return send_file(image_stream, mimetype='image/jpeg', as_attachment=True, download_name='photo.jpg')
    except Exception as e:
        return jsonify({"status": f"Error capturing photo: {str(e)}"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)