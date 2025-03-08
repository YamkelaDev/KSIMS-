from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import os

app = Flask(__name__)
app.secret_key = 'secure_key_here'

# Folder for storing files
UPLOAD_FOLDER = 'documents'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure folders exist
def create_default_folders():
    folder_structure = {
        'Filing System': ['Finance', 'HR', 'Projects', 'Legal'],
        'Expense Tracker': []
    }
    for main_folder, subfolders in folder_structure.items():
        main_path = os.path.join(UPLOAD_FOLDER, main_folder)
        os.makedirs(main_path, exist_ok=True)
        for subfolder in subfolders:
            os.makedirs(os.path.join(main_path, subfolder), exist_ok=True)

# Home Page - Welcoming Message
@app.route('/')
def home():
    return render_template('welcome.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # TODO: Implement user authentication
        session['user'] = email  # Temporary
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# User Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['user'])

# Filing System Page
@app.route('/filing_system')
def filing_system():
    folders = os.listdir(os.path.join(app.config['UPLOAD_FOLDER'], 'Filing System'))
    return render_template('filing_system.html', folders=folders)

# Expense Tracker Page
@app.route('/expense_tracker')
def expense_tracker():
    return render_template('expense_tracker.html')

# Run App
if __name__ == '__main__':
    create_default_folders()
    app.run(debug=True)
