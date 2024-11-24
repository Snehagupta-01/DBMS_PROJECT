from flask import Flask, session, redirect, url_for, jsonify,request
import mysql.connector
from functools import wraps

app = Flask(__name__)

# Secret key for session encryption (you can set it to any secret string)
app.secret_key = 'your_secret_key'

# MySQL connection function
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',        # MySQL host (e.g., localhost)
        user='root',             # MySQL username
        password='2006',  # MySQL password
        database='DBMS_PROJECT'    # Database name
    )

# Decorator to protect routes that require login
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):  # Check if user_id exists in session
            return redirect(url_for('user.login'))  # Redirect to login if not logged in
        return func(*args, **kwargs)
    return wrapper

# Route to login (for testing purposes)
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Connect to the database
    db = get_db_connection()
    cursor = db.cursor()

    # SQL query to check if the user exists and verify credentials
    query = "SELECT user_id, password FROM Users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    if user and user[1] == password:  # Check if password matches (simplified, in production use hashed passwords)
        session['user_id'] = user[0]  # Store user_id in session
        return redirect(url_for('user.profile'))  # Redirect to the user profile page
    else:
        return jsonify({'error': 'Invalid credentials'}), 400

# Route to view user profile (protected by login_required)
@app.route('/profile')
@login_required
def profile():
    user_id = session.get('user_id')  # Retrieve user_id from the session

    # Connect to the database
    db = get_db_connection()
    cursor = db.cursor()

    # SQL query to get the user's details from the database
    query = "SELECT username, email FROM Users WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()

    if user:
        return jsonify({'username': user[0], 'email': user[1]})
    else:
        return jsonify({'error': 'User not found'}), 404

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True,port=5002)
