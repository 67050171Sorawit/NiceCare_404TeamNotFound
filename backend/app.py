from flask import Flask, render_template, request, redirect, Response
import sqlite3
import os
import cv2
import requests
import numpy as np
import time

import firebase_admin
from firebase_admin import credentials, db


# =========================
# FLASK CONFIG
# =========================
app = Flask(
    __name__,
    template_folder='../frontend/templates',
    static_folder='../frontend/static'
)


# =========================
# ESP32 CAMERA
# =========================
ESP32_URL = "http://10.194.23.33/capture"


# =========================
# DATABASE
# =========================
def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        camera_url TEXT
    )
    """)

    conn.commit()
    conn.close()


create_db()


# =========================
# FIREBASE
# =========================
cred = credentials.Certificate("firebase_key.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL": "https://nice-care-4fa00-default-rtdb.asia-southeast1.firebasedatabase.app/"
        }
    )


# =========================
# CAMERA STREAM
# =========================
def generate_frames():
    while True:
        try:
            response = requests.get(ESP32_URL, timeout=0.5)

            if response.status_code != 200:
                continue

            frame = response.content

            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n'
                + frame +
                b'\r\n'
            )

            time.sleep(0.5)

        except Exception as e:
            print("STREAM ERROR:", e)
            continue


@app.route("/video")
def video():
    print("VIDEO ROUTE OPENED")

    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


# =========================
# HOME
# =========================
@app.route("/")
def welcome():
    return render_template("welcome.html")


# =========================
# LOGIN
# =========================
@app.route("/login")
def login():
    return render_template("login.html")


# =========================
# REGISTER
# =========================
@app.route("/register")
def register():
    return render_template("register.html")


# =========================
# REGISTER USER
# =========================
@app.route("/register_user", methods=["POST"])
def register_user():

    username = request.form.get("username")
    password = request.form.get("password")
    camera_url = request.form.get("camera_url")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO users VALUES(NULL,?,?,?)
    """, (username, password, camera_url))

    conn.commit()
    conn.close()

    return redirect("/login")


# =========================
# DASHBOARD (FIXED)
# =========================
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    fall_status = "NORMAL"
    fall_time = "-"

    # ===== Firebase NORMAL LOAD =====
    try:
        ref = db.reference("/fall_status")
        data = ref.get()

        if data:
            fall_status = data.get("status", "NORMAL")
            fall_time = data.get("time", "-")

    except Exception as e:
        print("Firebase error:", e)

    alerts = [
        "10:30 - Normal",
        "11:00 - Normal",
        "11:15 - Fall Detected"
    ]

    username = "Guest"

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute("""
            SELECT *
            FROM users
            WHERE username=?
            AND password=?
        """, (username, password))

        user = c.fetchone()
        conn.close()

        if not user:
            return "<h1>Login Failed</h1>"

    return render_template(
        "index.html",
        username=username,
        camera_status="ONLINE",
        fall_status=fall_status,
        fall_time=fall_time,
        alerts=alerts
    )


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    return redirect("/")


# =========================
# CALL PAGE
# =========================
@app.route("/one-tap-call")
def one_tap_call():
    return app.send_static_file("one-tap-call.html")


# =========================
# RUN
# =========================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True,
        threaded=True
    )