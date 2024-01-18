from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    root_path = '/home/laika'  # Replace with the path to your shared folder
    files = os.listdir(root_path)
    directories = [d for d in os.listdir(root_path) if os.path.isdir(os.path.join(root_path, d))]
    return render_template('index.html', files=files)

@app.route('/files/<path:filename>')
def serve_file(filename):
    root_path = '/home/laika'  # Replace with the path to your shared folder
    return send_from_directory(root_path, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)
