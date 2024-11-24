# Organ-Donation-and-Procurement-Network-Management-System

1.Set Up Virtual Environment Create a virtual environment: python -m venv venv.

2.Activate the virtual environment: For Windows: venv\Scripts\activate

3.Configure app_runner.py Locate the python.exe file inside the venv/Scripts/ folder. Copy its full path and replace it in the app_runner.py file

4.Install Required Dependencies Install all dependencies from requirements.txt: pip install -r requirements.txt 

5.Configure MySQL Connection Open app.py files in user_app, shared, donor_app, and patient_app. Update the MySQL password to match your system's configuration.

6.Create the Database In the MySQL command line or MySQL Workbench, run the following command: CREATE DATABASE DBMS_PROJECT;

7.Initialize and Migrate the Database Navigate to the shared directory: cd shared Run the following commands: flask db init flask db migrate flask db upgrade (if needed otherwise this step is not mandatory)

8.Go to the project root directory and run the command: python app_runner.py
