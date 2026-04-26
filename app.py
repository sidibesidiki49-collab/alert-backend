from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
from db import init_db

app = Flask(__name__)
CORS(app)

init_db()

@app.route("/alert", methods=["POST"])
def create_alert():
    data = request.json

    conn = sqlite3.connect("alerts.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO alerts (type, message, latitude, longitude, date)
    VALUES (?, ?, ?, ?, ?)
    """, (
        data["type"],
        data["message"],
        data["lat"],
        data["lng"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})


@app.route("/alerts", methods=["GET"])
def get_alerts():
    conn = sqlite3.connect("alerts.db")
    c = conn.cursor()

    c.execute("SELECT * FROM alerts ORDER BY id DESC")
    rows = c.fetchall()

    conn.close()

    return jsonify(rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)