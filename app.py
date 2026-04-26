from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# 📦 Initialisation base de données
def init_db():
    conn = sqlite3.connect("alerts.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT,
        message TEXT,
        latitude TEXT,
        longitude TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# 🚨 Route pour créer une alerte
@app.route("/alert", methods=["POST"])
def create_alert():
    data = request.json

    conn = sqlite3.connect("alerts.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO alerts (type, message, latitude, longitude, date)
    VALUES (?, ?, ?, ?, ?)
    """, (
        data.get("type"),
        data.get("message"),
        data.get("lat"),
        data.get("lng"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return jsonify({"status": "ok"})


# 📊 Route pour récupérer les alertes
@app.route("/alerts", methods=["GET"])
def get_alerts():
    conn = sqlite3.connect("alerts.db")
    c = conn.cursor()

    c.execute("SELECT * FROM alerts ORDER BY id DESC")
    rows = c.fetchall()

    conn.close()

    return jsonify(rows)


# 🟢 Route test
@app.route("/")
def home():
    return "API ALERT BACKEND RUNNING"


# 🚀 Lancement compatible Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)