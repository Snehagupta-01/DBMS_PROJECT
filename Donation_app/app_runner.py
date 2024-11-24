from flask import Flask
import subprocess
from user_app.routes import user_blueprint
from donor_app.routes import donor_blueprint
from patient_app.routes import patient_blueprint

app = Flask(__name__)
app.secret_key = 'sec key'

# Register blueprints for modular routing
app.register_blueprint(user_blueprint, url_prefix='/user')
app.register_blueprint(donor_blueprint, url_prefix='/donor')
app.register_blueprint(patient_blueprint, url_prefix='/patient')

def run_app_1_service():
    subprocess.Popen(["C:\\Users\\asus\\OneDrive\\Desktop\\Donation_app\\venv\\Scripts\\python", "donor_app\\routes.py"])

def run_app_2_service():
    subprocess.Popen(["C:\\Users\\asus\\OneDrive\\Desktop\\Donation_app\\venv\\Scripts\\python", "patient_app\\routes.py"])

def run_app_3_service():
    subprocess.Popen(["C:\\Users\\asus\\OneDrive\\Desktop\\Donation_app\\venv\\Scripts\\python", "shared\\session_utlis.py"])

def run_app_4_service():
    subprocess.Popen(["C:\\Users\\asus\\OneDrive\\Desktop\\Donation_app\\venv\\Scripts\\python", "user_app\\routes.py"])

if __name__ == '_main_':
    run_app_1_service()
    run_app_2_service()
    run_app_3_service()
    run_app_4_service()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nTerminating all processes. Alvida!")