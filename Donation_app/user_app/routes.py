from flask import Flask, Blueprint, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash  # Import for password hashing

# Set up Flask app
app = Flask(__name__)

# Secret key for session encryption
app.secret_key = 'your_secret_key'

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2006@localhost/DBMS_PROJECT'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# SQLAlchemy model for User table
class User(db.Model):
    __tablename__ = 'login'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

# Set up Blueprint for user routes
user_blueprint = Blueprint('user', __name__)

# Route for user login (POST)
@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Get JSON data from request body
    username = data.get('username')
    password = data.get('password')

    # Check if username and password are provided
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # Query the database using SQLAlchemy
    user = User.query.filter_by(username=username).first()

    # Check if the user exists and password matches
    if not user or user.password != password:
        return jsonify({"error": "Invalid credentials"}), 401

    # Store session data
    session['login'] = True
    session['username'] = username
    session['isAdmin'] = (username == 'admin')

    return jsonify({"message": "Login successful!"}), 200

# Route for user logout (clear session)
@user_blueprint.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear all session data
    return jsonify({"message": "Logged out successfully!"}), 200

# Route for the dashboard (GET)
@user_blueprint.route('/dashboard', methods=['GET'])
def dashboard():
    if not session.get('login'):  # Check if the user is logged in
        return jsonify({"error": "Unauthorized access"}), 401  # Unauthorized response

    # Get the username from session
    username = session.get('username')
    return jsonify({"message": f"Welcome, {username}!", "isAdmin": session.get('isAdmin')}), 200

# Route for user registration (POST)
@user_blueprint.route('/register', methods=['POST'])
def register_user():
    # Get data from the POST request body
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    # Check if username and password are provided
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # Check if the username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    # Hash the password before storing it
    hashed_password = generate_password_hash(password)

    # Create a new user and store it in the database
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully!"}), 201

# Register blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')

# Run the Flask app
if __name__ == '__main__':
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5003)
