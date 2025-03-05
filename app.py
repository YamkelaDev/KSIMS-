from flask import Flask, render_template, request, redirect, url_for, flash
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'Sister_Bethina'
UPLOAD_FOLDER = 'documents'
GIT_REPO_PATH = '/YamkelaDev/KSIMS-/' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def git_sync(commit_message):
    try:
        subprocess.run(['git', 'add', '.'], cwd=GIT_REPO_PATH, check=True)
        subprocess.run(['git', 'commit', '-m', commit_message], cwd=GIT_REPO_PATH, check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], cwd=GIT_REPO_PATH, check=True)
    except subprocess.CalledProcessError as e:
        print(f'Git error: {e}')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(request.url)
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    git_sync(f'Added {filename}')
    flash('File uploaded successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/create_folder', methods=['POST'])
def create_folder():
    folder_name = request.form.get('folder_name', '').strip()
    if not folder_name:
        flash('Folder name cannot be empty', 'danger')
        return redirect(url_for('home'))
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
    os.makedirs(folder_path, exist_ok=True)
    git_sync(f'Created folder {folder_name}')
    flash(f'Folder "{folder_name}" created successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
