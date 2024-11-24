from flask import Flask, session, redirect, url_for, jsonify, request
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

# Set up Flask app
app = Flask(__name__)

# Secret key for session encryption
app.secret_key = 'your_secret_key'

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2006@localhost/DBMS_PROJECT'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# SQLAlchemy model for Users
class User(db.Model):
    __tablename__ = 'Users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

# Decorator to protect routes that require login
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):  # Check if user_id exists in session
            return jsonify({'error': 'Unauthorized access'}), 401  # Respond with unauthorized status
        return func(*args, **kwargs)
    return wrapper

# Route to login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Accept JSON input
    username = data.get('username')
    password = data.get('password')

    # Query the database for the user
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:  # Verify password
        session['user_id'] = user.user_id  # Store user_id in session
        return jsonify({'message': 'Login successful', 'username': username}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 400

# Route to view user profile (protected by login_required)
@app.route('/profile', methods=['GET'])
@login_required
def profile():
    user_id = session.get('user_id')  # Retrieve user_id from session

    # Query the database for the user's details
    user = User.query.get(user_id)

    if user:
        return jsonify({'username': user.username, 'email': user.email}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# Run the Flask app
if __name__ == '__main__':
    # Create all tables if they don't exist
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5002)
