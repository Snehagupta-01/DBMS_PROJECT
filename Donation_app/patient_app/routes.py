from flask import Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Set up Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:2006@localhost/DBMS_PROJECT'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Patient model
class Patient(db.Model):
    __tablename__ = 'Patient'
    
    patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_name = db.Column(db.String(100), nullable=False)
    organ_req = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "patient_name": self.patient_name,
            "organ_req": self.organ_req
        }

# Set up Blueprint for patient routes
patient_blueprint = Blueprint('patient', __name__)

# Route to add a patient to the database (POST)
@patient_blueprint.route('/add', methods=['POST'])
def add_patient():
    # Get JSON data from the request body
    data = request.get_json()

    # Extract values from JSON data
    patient_name = data.get('patient_name')
    organ_req = data.get('organ_req')

    # Validate input data
    if not patient_name or not organ_req:
        return jsonify({"error": "Missing required fields: patient_name, organ_req"}), 400

    # Create a new Patient object
    new_patient = Patient(patient_name=patient_name, organ_req=organ_req)
    
    try:
        # Add to database session and commit
        db.session.add(new_patient)
        db.session.commit()
        return jsonify({"message": "Patient added successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Route to view all patients (GET)
@patient_blueprint.route('/view', methods=['GET'])
def view_patients():
    try:
        # Query all patients from the database
        patients = Patient.query.all()

        # Convert the patient objects to a list of dictionaries
        patients_list = [patient.to_dict() for patient in patients]

        return jsonify(patients_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Register blueprint
app.register_blueprint(patient_blueprint, url_prefix='/patient')

# Run the Flask app
if __name__ == '__main__':
    # Ensure the database tables are created
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
