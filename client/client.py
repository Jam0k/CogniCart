from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/receive', methods=['POST'])
def receive_command():
    command = request.json.get('command')
    # Process the command here and perform actions on the Raspberry Pi
    return jsonify({"message": f"Command '{command}' received and executed"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
