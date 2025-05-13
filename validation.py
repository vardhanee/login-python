from flask import Flask, request, jsonify, send_from_directory
import re
import os  # Import the os module
from flask_cors import CORS  # Import CORS for cross-origin requests
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.before_request
def log_request_info():
    logging.debug(f"Headers: {request.headers}")
    logging.debug(f"Body: {request.get_data()}")

def is_valid_username(username):
    if not username:
        return False, "Username cannot be empty."
    if len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if len(username) > 20:
        return False, "Username cannot be longer than 20 characters."
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain alphanumeric characters and underscores."
    return True, None

def is_valid_password(password):
    if not password:
        return False, "Password cannot be empty."
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit."
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character."
    return True, None

@app.route('/')
def serve_login_page():
    # Serve the login.html file
    return send_from_directory('.', 'login.html')

@app.route('/<path:filename>')
def serve_static_files(filename):
    # Serve static files like styles.css
    return send_from_directory('.', filename)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    username_valid, username_error = is_valid_username(username)
    password_valid, password_error = is_valid_password(password)

    if username_valid and password_valid:
        # In a real application, you would check against a database here
        # For demonstration purposes, let's use hardcoded credentials
        if username == "testuser" and password == "SecurePassword123!":
            return jsonify({'success': True, 'message': 'Login successful!'}), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401
    else:
        errors = {}
        if username_error:
            errors['username'] = username_error
        if password_error:
            errors['password'] = password_error
        return jsonify({'success': False, 'errors': errors, 'message': 'Validation failed.'}), 400

if __name__ == '__main__':
    # Run the app on the port Heroku assigns
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)