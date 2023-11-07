import io
from flask import Flask, jsonify, render_template, send_file, Response
import requests
from io import BytesIO
import shutil
import os
import base64
from threading import Thread

app = Flask(__name__)

# A list containing the URLs of the Raspberry Pi devices
raspberry_pis = [
    "http://86.8.33.63:5004",
    "http://86.8.33.63:5003",
    "http://86.8.33.63:5002",
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
    
@app.route('/api/consume_stream/<int:device_id>', methods=['GET'])
def consume_stream(device_id):
    try:
        pi_url = raspberry_pis[device_id-1]
        response = requests.get(f"{pi_url}/api/stream_photos", stream=True)

        if response.status_code == 200:
            image_num = 0
            image_file = None  # Initializing image_file

            # Ensure the directory exists
            if not os.path.exists('received_images'):
                os.makedirs('received_images')

            for chunk in response.iter_content(chunk_size=8192):
                if chunk.startswith(b'--frame'):  # This is the boundary between images
                    if image_file:  # If an image file is open, close it
                        image_file.close()

                    # Open a new file for writing the next image
                    image_num += 1
                    image_filename = f"image_{device_id}_{image_num}.jpg"
                    image_file = open(os.path.join('received_images', image_filename), 'wb')

                if image_file:
                    image_file.write(chunk)
                    image_file.flush()  # Flush the buffer

            if image_file:  # Close the last image file if it exists
                image_file.close()

            return jsonify({"status": "Images saved successfully."})

        else:
            return jsonify({"error": "Failed to consume stream, invalid status code."})

    except requests.exceptions.RequestException as e:
        if image_file:  # Ensure the image file is closed in case of an error
            image_file.close()
        return jsonify({"error": f"Failed to consume stream: {str(e)}"})
    
@app.route('/api/take_photos_all', methods=['GET'])
def take_photos_all():
    def capture_image(pi_url, photos_data, device_id):
        try:
            response = requests.get(f"{pi_url}/api/take_photo", stream=True)

            if response.status_code == 200:
                photos_data.append({
                    "client_id": f"Client {device_id}",
                    "photo": base64.b64encode(response.content).decode('utf-8')  # Encoding the photo in base64
                })
            else:
                photos_data.append({
                    "client_id": f"Client {device_id}",
                    "error": "Failed to capture photo, invalid status code."
                })

        except requests.exceptions.RequestException as e:
            photos_data.append({
                "client_id": f"Client {device_id}",
                "error": f"Failed to capture photo: {str(e)}"
            })

    threads = []
    photos_data = []

    # Start a thread for each Raspberry Pi
    for device_id, pi_url in enumerate(raspberry_pis, start=1):
        thread = Thread(target=capture_image, args=(pi_url, photos_data, device_id))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return jsonify(photos_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
