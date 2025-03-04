import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.secret_key = 'Sister_bethina'  # Use a secure key in production
app.config['UPLOAD_FOLDER'] = 'documents'

# Ensure base upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Predefined folder structure
FOLDER_STRUCTURE = {
    'employees': ['contracts', 'personal_info'],
    'farmers': ['contracts', 'personal_info'],
    'procurements': ['invoices', 'purchase_orders'],
    'pictures': ['events', 'meetings'],
    'reports': ['financial', 'activity'],
    'administration': ['policies', 'guidelines'],
    'performance_monitors': ['individual', 'team'],
    'evaluation': ['reviews', 'assessments']
}

# Create predefined folders
for main_folder, subfolders in FOLDER_STRUCTURE.items():
    main_path = os.path.join(app.config['UPLOAD_FOLDER'], main_folder)
    os.makedirs(main_path, exist_ok=True)
    for subfolder in subfolders:
        sub_path = os.path.join(main_path, subfolder)
        os.makedirs(sub_path, exist_ok=True)

@app.route('/')
def home():
    return "Welcome to KwaZulu Natal Spice Initiative Management System!"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/create_folder', methods=['POST'])
def create_folder():
    data = request.json
    folder_name = data.get('folder_name')
    parent_folder = data.get('parent_folder', '')

    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], parent_folder, folder_name) if parent_folder else os.path.join(app.config['UPLOAD_FOLDER'], folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return jsonify({"message": "Folder created successfully", "path": folder_path}), 201
    else:
        return jsonify({"error": "Folder already exists"}), 400

@app.route('/list_folders', methods=['GET'])
def list_folders():
    folders = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    return jsonify({"folders": folders})

@app.route('/upload_file/<main_folder>/<subfolder>', methods=['POST'])
def upload_file(main_folder, subfolder):
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], main_folder, subfolder)
    if not os.path.exists(folder_path):
        return jsonify({"error": "Folder does not exist"}), 400

    filename = secure_filename(file.filename)
    file.save(os.path.join(folder_path, filename))

    return jsonify({"message": "File successfully uploaded", "path": os.path.join(folder_path, filename)}), 201

@app.route('/delete_file/<main_folder>/<subfolder>/<filename>', methods=['DELETE'])
def delete_file(main_folder, subfolder, filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], main_folder, subfolder, filename)
    
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": "File deleted successfully"}), 200
    else:
        return jsonify({"error": "File not found"}), 404

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf', 'png', 'jpg', 'jpeg', 'gif'}

if __name__ == "__main__":
    app.run(debug=True)
