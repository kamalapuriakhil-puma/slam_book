from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS slam_entries ("
    "id SERIAL PRIMARY KEY,"
    "name TEXT,"
    "message TEXT)"
)
conn.commit()
cur.close()

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO slam_entries (name, message) VALUES (%s, %s)",
        (data["name"], data["message"])
    )
    conn.commit()
    cur.close()
    return {"status": "saved"}

@app.route("/entries", methods=["GET"])
def entries():
    cur = conn.cursor()
    cur.execute("SELECT name, message FROM slam_entries")
    rows = cur.fetchall()
    cur.close()
    return jsonify(rows)

app.run(host="0.0.0.0", port=5000)
