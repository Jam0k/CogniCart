from flask import Flask, jsonify
import psutil

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
