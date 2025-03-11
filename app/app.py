from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

# Fetch database credentials from ConfigMap and Secret
DB_HOST = os.getenv("DB_HOST", "postgres-service")  # From ConfigMap
DB_NAME = os.getenv("DB_NAME", "mydatabase")  # From ConfigMap
DB_USER = os.getenv("DB_USER", "admin")  # From Secret
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")  # From Secret

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)

@app.route('/')
def index():
    return jsonify({"message": "Flask App is Running!"})

@app.route('/users')
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
