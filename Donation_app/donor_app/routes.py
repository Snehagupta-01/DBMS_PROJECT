from flask import Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Set up Flask app
app = Flask(__name__)

# SQLAlchemy Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2006@localhost/DBMS_PROJECT'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Donor model
class Donor(db.Model):
    __tablename__ = 'Donor'
    donor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donor_name = db.Column(db.String(100), nullable=False)
    organ = db.Column(db.String(100), nullable=False)
    reason = db.Column(db.String(255), nullable=False)

    def __init__(self, donor_name, organ, reason):
        self.donor_name = donor_name
        self.organ = organ
        self.reason = reason

# Initialize the database (you should create tables beforehand using migrations or `db.create_all()`)
# db.create_all() can be used temporarily for quick testing

# Set up Blueprint for donor routes
donor_blueprint = Blueprint('donor', __name__)

# Route to add a donor to the database (POST)
@donor_blueprint.route('/add', methods=['POST'])
def add_donor():
    # Get JSON data from the request body
    data = request.get_json()
    
    # Extract values from JSON data
    donor_name = data.get('donor_name')
    organ = data.get('organ')
    reason = data.get('reason')

    # Validate input data
    if not donor_name or not organ or not reason:
        return jsonify({"error": "Missing required fields: donor_name, organ, reason"}), 400

    # Create a new Donor instance
    new_donor = Donor(donor_name=donor_name, organ=organ, reason=reason)
    
    try:
        db.session.add(new_donor)
        db.session.commit()
        return jsonify({"message": "Donor added successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Route to view all donors (GET)
@donor_blueprint.route('/view', methods=['GET'])
def view_donors():
    try:
        # Query all donors from the database
        donors = Donor.query.all()

        # Convert the donor data into a list of dictionaries
        donors_list = []
        for donor in donors:
            donors_list.append({
                "donor_id": donor.donor_id,
                "donor_name": donor.donor_name,
                "organ": donor.organ,
                "reason": donor.reason,
            })

        return jsonify(donors_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Register blueprint
app.register_blueprint(donor_blueprint, url_prefix='/donor')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
