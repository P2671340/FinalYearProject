from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import subprocess
import json

#Import from the custom modules
from scanner import check_system_resources
from azure_check import check_azure_vms
from security_check import check_open_ports

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

#Health check route
@app.route('/health')
def health_check():
    return "OK", 200

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('user'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['username'] = username
            return redirect(url_for('user'))
        else:
            return "Login Failed. Invalid credentials."
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash("yourpassword", method="ppkdf2:sha256")
        print(hashed_password)

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/user')
def user():
    if 'username' in session:
        username = session['username']
        return render_template('user.html', username=username)
    else:
        return redirect(url_for('login'))


@app.route('/run-scan')
def run_scan():
    if 'username' in session:
        # System resource checks
        system_misconfigurations = check_system_resources()

        # Azure misconfiguration checks
        azure_misconfigurations = check_azure_vms()

        # Security Checks
        security_issues = check_open_ports()


        # Use subprocess to run the Node.js script and capture the output
        try:
            result = subprocess.run(
                ['node', 'index.js', '--json=./output.json'],  # Adjust script and output format as needed
                capture_output=True,
                text=True,
                check=True
            )

            # Load JSON output from the file
            with open('output.json', 'r') as f:
                scan_data = json.load(f)
            
            # Combine all findings into the result
            scan_data['system_misconfigurations'] = system_misconfigurations
            scan_data['azure_misconfigurations'] = azure_misconfigurations
            scan_data['security_issues'] = security_issues

            # Return the scan results as a JSON response
            return jsonify(scan_data)  # This sends the scan data as JSON

        except subprocess.CalledProcessError as e:
            return f"Error running scan: {e.output}"

    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Default to 8000
    app.run(host="0.0.0.0", port=port, debug=False)