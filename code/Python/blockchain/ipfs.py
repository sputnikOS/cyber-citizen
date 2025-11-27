import ipfshttpclient
from flask import Flask, request, jsonify

app = Flask(__name__)
client = ipfshttpclient.connect()  # Connect to local IPFS node

@app.route('/add', methods=['POST'])
def add_file():
    """Add a file to IPFS."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        result = client.add(file)
        return jsonify({
            "hash": result["Hash"],
            "name": result["Name"],
            "size": result["Size"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get/<file_hash>', methods=['GET'])
def get_file(file_hash):
    """Retrieve a file from IPFS."""
    try:
        content = client.cat(file_hash)
        return content, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/pin/<file_hash>', methods=['POST'])
def pin_file(file_hash):
    """Pin a file to the local IPFS node."""
    try:
        client.pin.add(file_hash)
        return jsonify({"message": f"File {file_hash} pinned successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/unpin/<file_hash>', methods=['POST'])
def unpin_file(file_hash):
    """Unpin a file from the local IPFS node."""
    try:
        client.pin.rm(file_hash)
        return jsonify({"message": f"File {file_hash} unpinned successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
