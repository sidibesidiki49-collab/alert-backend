from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os
import requests

from google.oauth2 import service_account
import google.auth.transport.requests

app = Flask(__name__)
CORS(app)

# 🔥 TON TOKEN CHEF (déjà inséré)
CHEF_TOKEN = "eN_cEYaRRgOL3MWCyzIGcJ:APA91bFL407Eyce3M2BvrQSMasPGpkeRR9UCpOj-HW_jZXYdgEe-hdeu_PxqJPBjWBujbdKof8goS7y6-szm_jRI4a9gIPJF40X8ZzDJos6_y0zODsbcQWE"

# 🔥 TON PROJECT ID
PROJECT_ID = "zeusalert-229fc"


# 📦 INIT DB
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


# 🔑 TOKEN GOOGLE
def get_access_token():
    credentials = service_account.Credentials.from_service_account_file(
        "serviceAccountKey.json",
        scopes=["https://www.googleapis.com/auth/firebase.messaging"]
    )

    request = google.auth.transport.requests.Request()
    credentials.refresh(request)

    return credentials.token


# 🔔 ENVOI NOTIFICATION
def send_notification(token, title, body):
    access_token = get_access_token()

    url = f"https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {
        "message": {
            "token": token,
            "notification": {
                "title": title,
                "body": body
            }
        }
    }

    response = requests.post(url, json=data, headers=headers)
    print("FCM RESPONSE:", response.text)


# 🚨 CREATE ALERT
@app.route("/alert", methods=["POST"])
def create_alert():
    data = request.json
    message = data.get("message", "Alerte inconnue")

    conn = sqlite3.connect("alerts.db")
    c = conn.cursor()

    c.execute("""
    INSERT INTO alerts (type, message, latitude, longitude, date)
    VALUES (?, ?, ?, ?, ?)
    """, (
        data.get("type"),
        message,
        data.get("lat"),
        data.get("lng"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    # 🔥 ENVOI NOTIFICATION
    send_notification(
        CHEF_TOKEN,
        "🚨 ALERTE ZEUS",
        message
    )

    return jsonify({"status": "alerte envoyée"})


# 📊 GET ALERTS
@app.route("/alerts", methods=["GET"])
def get_alerts():
    conn = sqlite3.connect("alerts.db")
    c = conn.cursor()

    c.execute("SELECT * FROM alerts ORDER BY id DESC")
    rows = c.fetchall()

    conn.close()

    return jsonify(rows)


# 🧪 TEST
@app.route("/test-alert")
def test_alert():
    send_notification(
        CHEF_TOKEN,
        "🚨 TEST ZEUS",
        "Notification OK 🔥"
    )
    return "Notification envoyée"


# 🟢 HOME
@app.route("/")
def home():
    return "ZEUS BACKEND ACTIF"


# 🚀 RUN
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)