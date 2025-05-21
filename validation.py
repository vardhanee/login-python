from flask import Flask, request, jsonify, send_from_directory
import re
import os
from flask_cors import CORS
import logging
import mysql.connector  # Import the MySQL connector
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)

# Database Configuration (Replace with your XAMPP MySQL credentials)
db_config = {
    'user': 'root',  # Changed from 'rrot' to 'root'
    'password': '',
    'host': 'localhost',
    'database': 'my_app_db'
}


def log_request_info():
    logging.debug(f"Headers: {request.headers}")
    logging.debug(f"Body: {request.get_data()}")


def connect_to_db():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn, conn.cursor()
    except mysql.connector.Error as err:
        logging.error(f"Database connection error: {err}")
        return None, None


def close_db_connection(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


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
        conn, cursor = connect_to_db()
        if not conn:
            return jsonify({'success': False, 'message': 'Database connection failed.'}), 500

        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user and user[2] == password:  # Assuming password is the 3rd column
                return jsonify({'success': True, 'message': 'Login successful!'}), 200
            else:
                return jsonify({'success': False, 'message': 'Invalid username or password.'}), 401

        except mysql.connector.Error as err:
            logging.error(f"Database query error: {err}")
            return jsonify({'success': False, 'message': 'Database error during login.'}), 500

        finally:
            close_db_connection(conn, cursor)

    else:
        errors = {}
        if username_error:
            errors['username'] = username_error
        if password_error:
            errors['password'] = password_error
        return jsonify({'success': False, 'errors': errors, 'message': 'Validation failed.'}), 400


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    gender = data.get('gender')
    dob_str = data.get('dob')  # Get DOB as string

    try:
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()  # Convert string to date
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid date format. Use YYYY-MM-DD'}), 400

    username_valid, username_error = is_valid_username(username)
    password_valid, password_error = is_valid_password(password)

    if username_valid and password_valid:
        conn, cursor = connect_to_db()
        if not conn:
            return jsonify({'success': False, 'message': 'Database connection failed.'}), 500

        try:
            cursor.execute(
                "INSERT INTO users (username, password, role, gender, dob) VALUES (%s, %s, %s, %s, %s)",
                (username, password, role, gender, dob)  # Use the date object
            )
            conn.commit()
            return jsonify({'success': True, 'message': 'Signup successful!'}), 201

        except mysql.connector.Error as err:
            logging.error(f"Database error during signup: {err}")
            conn.rollback()
            return jsonify({'success': False, 'message': 'Database error during signup.'}), 500

        finally:
            close_db_connection(conn, cursor)

    else:
        errors = {}
        if username_error:
            errors['username'] = username_error
        if password_error:
            errors['password'] = password_error
        return jsonify({'success': False, 'errors': errors, 'message': 'Validation failed.'}), 400


@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    username_or_email = data.get('usernameOrEmail')

    #   logic to handle forgot password
    #   For demonstration purposes, we'll just return a success message
    return jsonify({'success': True, 'message': 'Password reset functionality is not implemented in this demo.'}), 200


if __name__ == '__main__':
    # Run the app on the port Heroku assigns
    port = int(os.environ.get('PORT', 5500))
    app.run(debug=True, host='0.0.0.0', port=port)