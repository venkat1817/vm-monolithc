import boto3
from botocore.exceptions import ClientError
from flask import Flask, jsonify
import json
import mysql.connector
import configparser

app = Flask(__name__)

# Create a configparser object
config = configparser.ConfigParser()

# Read the properties file
config.read('properties.db')

# Access the values from the 'database' section
user = config.get('database', 'user')
password = config.get('database', 'password')
host = config.get('database', 'host')
database = config.get('database', 'database')

# Establish the MySQL connection
cnx = mysql.connector.connect(
    user=user,
    password=password,
    host=host,
    database=database
)


def execute_query(query):
    # Execute a query on the database connection
    cursor = cnx.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    return response


@app.route('/employee')
def index():
    # Execute a query to retrieve data from the "employee" table
    query = "SELECT * FROM employees"
    rows = execute_query(query)

    # Convert the data to a list of dictionaries
    results = []
    for row in rows:
        result = {
            'id': row[0],
            'name': row[1],
            'position': row[2],
            # Add more fields as needed
        }
        results.append(result)

    # Return the data as JSON
    return jsonify(results)


@app.route('/student')
def home():
    # Execute a query to retrieve data from the "student" table
    query = "SELECT * FROM student"
    rows = execute_query(query)

    # Convert the data to a list of dictionaries
    results = []
    for row in rows:
        result = {
            'id': row[0],
            'name': row[1],
            'age': row[2],
            # Add more fields as needed
        }
        results.append(result)

    # Return the data as JSON
    return jsonify(results)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
