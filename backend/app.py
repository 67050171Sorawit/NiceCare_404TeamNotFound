from flask import Flask, render_template, request, redirect, Response, jsonify
import sqlite3
import os
import time
import threading

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
# CAMERA FRAME BUFFER (ESP32 push เข้ามาเก็บไว้ตรงนี้)
# =========================
latest_frame = None          # bytes ของภาพล่าสุด
latest_frame_time = 0        # timestamp ของภาพล่าสุด (วินาที)
frame_lock = threading.Lock()
FRAME_STALE_SECONDS = 10      # ถ้าไม่มีภาพใหม่เกิน 10 วิ ถือว่ากล้องออฟไลน์


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

    c.execute("""
    CREATE TABLE IF NOT EXISTS contacts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL
    )
    """)

    # ใส่ข้อมูลตัวอย่างถ้ายังไม่มี
    c.execute("SELECT COUNT(*) FROM contacts")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO contacts(name, phone) VALUES(?,?)", [
            ("ลูกชาย",  "0812345678"),
            ("ลูกสาว",  "0898765432"),
            ("ผู้ดูแล", "0851112222"),
            ("แทร 1669", "1669"),
        ])

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
# HELPERS
# =========================
def get_contacts():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, name, phone FROM contacts ORDER BY id")
    rows = [{"id": r[0], "name": r[1], "phone": r[2]} for r in c.fetchall()]
    conn.close()
    return rows


# =========================
# CAMERA: ESP32 ส่งภาพเข้ามาที่นี่ (PUSH)
# =========================
@app.route("/upload-frame", methods=["POST"])
def upload_frame():
    """ESP32 เรียก endpoint นี้เป็นระยะ พร้อมแนบไฟล์ JPEG มาด้วย"""
    global latest_frame, latest_frame_time

    frame_bytes = request.get_data()  # ESP32 ส่งมาเป็น raw JPEG bytes ใน body

    if not frame_bytes:
        return jsonify({"ok": False, "error": "empty body"}), 400

    with frame_lock:
        latest_frame = frame_bytes
        latest_frame_time = time.time()

    return jsonify({"ok": True})


@app.route("/video")
def video():
    """Browser ดึงภาพล่าสุดจากที่นี่ — ไม่ได้วิ่งไปหา ESP32 ตรงๆ อีกต่อไป"""
    with frame_lock:
        frame = latest_frame
        age = time.time() - latest_frame_time if latest_frame_time else None

    if frame is None or (age is not None and age > FRAME_STALE_SECONDS):
        return jsonify({"ok": False, "error": "no recent frame"}), 503

    return Response(frame, mimetype="image/jpeg")


@app.route("/api/camera-status")
def camera_status_api():
    """Dashboard ใช้เช็คว่ากล้องออนไลน์อยู่ไหม (ภาพมาไม่เกิน 10 วิ)"""
    with frame_lock:
        has_frame = latest_frame is not None
        age = time.time() - latest_frame_time if latest_frame_time else None

    online = has_frame and age is not None and age <= FRAME_STALE_SECONDS

    return jsonify({
        "online": online,
        "age_seconds": round(age, 1) if age is not None else None
    })


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
    username   = request.form.get("username")
    password   = request.form.get("password")
    camera_url = request.form.get("camera_url")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES(NULL,?,?,?)", (username, password, camera_url))
    conn.commit()
    conn.close()
    return redirect("/login")


# =========================
# API: FALL STATUS
# =========================
@app.route("/api/fall-status")
def fall_status_api():
    try:
        ref  = db.reference("/fall_status")
        data = ref.get()
        if data:
            return jsonify({
                "status": data.get("status", "NORMAL"),
                "time":   data.get("time",   "-")
            })
    except Exception as e:
        print("Firebase error:", e)
    return jsonify({"status": "NORMAL", "time": "-"})


# =========================
# DASHBOARD
# =========================
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    fall_status = "NORMAL"
    fall_time   = "-"

    try:
        ref  = db.reference("/fall_status")
        data = ref.get()
        if data:
            fall_status = data.get("status", "NORMAL")
            fall_time   = data.get("time",   "-")
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
        c    = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if not user:
            return "<h1>Login Failed</h1>"

    contacts = get_contacts()

    return render_template(
        "index.html",
        username=username,
        camera_status="ONLINE",
        fall_status=fall_status,
        fall_time=fall_time,
        alerts=alerts,
        contacts=contacts
    )


# =========================
# SETTINGS — จัดการผู้ติดต่อ
# =========================
@app.route("/settings")
def settings():
    contacts = get_contacts()
    return render_template("settings.html", contacts=contacts)


@app.route("/contacts/add", methods=["POST"])
def contact_add():
    name  = request.form.get("name",  "").strip()
    phone = request.form.get("phone", "").strip()
    if name and phone:
        conn = sqlite3.connect("users.db")
        c    = conn.cursor()
        c.execute("INSERT INTO contacts(name, phone) VALUES(?,?)", (name, phone))
        conn.commit()
        conn.close()
    return redirect("/settings")


@app.route("/contacts/edit/<int:cid>", methods=["POST"])
def contact_edit(cid):
    name  = request.form.get("name",  "").strip()
    phone = request.form.get("phone", "").strip()
    if name and phone:
        conn = sqlite3.connect("users.db")
        c    = conn.cursor()
        c.execute("UPDATE contacts SET name=?, phone=? WHERE id=?", (name, phone, cid))
        conn.commit()
        conn.close()
    return redirect("/settings")


@app.route("/contacts/delete/<int:cid>", methods=["POST"])
def contact_delete(cid):
    conn = sqlite3.connect("users.db")
    c    = conn.cursor()
    c.execute("DELETE FROM contacts WHERE id=?", (cid,))
    conn.commit()
    conn.close()
    return redirect("/settings")


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    return redirect("/")


# =========================
# CALL PAGE (legacy)
# =========================
@app.route("/one-tap-call")
def one_tap_call():
    return redirect("/settings")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, threaded=True)