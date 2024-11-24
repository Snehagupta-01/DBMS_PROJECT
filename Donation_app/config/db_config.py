import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='2006',
        database='DBMS_PROJECT'
    )
