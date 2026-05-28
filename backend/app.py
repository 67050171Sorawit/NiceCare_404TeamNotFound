from flask import Flask, render_template, request, redirect
import sqlite3
import os
import mediapipe as mp
import math

# =========================
# FIREBASE IMPORT
# =========================
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
# CREATE DATABASE
# =========================
def create_db():

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            camera_url TEXT
        )
    ''')

    conn.commit()
    conn.close()

create_db()

# =========================
# FIREBASE SETUP
# =========================
cred = credentials.Certificate("firebase_key.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://nice-care-4fa00-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# =========================
# WELCOME PAGE
# =========================
@app.route('/')
def welcome():

    return render_template('welcome.html')

# =========================
# LOGIN PAGE
# =========================
@app.route('/login')
def login():

    return render_template('login.html')

# =========================
# REGISTER PAGE
# =========================
@app.route('/register')
def register():

    return render_template('register.html')

# =========================
# REGISTER USER
# =========================
@app.route('/register_user', methods=['POST'])
def register_user():

    username = request.form.get('username')
    password = request.form.get('password')
    camera_url = request.form.get('camera_url')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()

    c.execute(
        '''
        INSERT INTO users(username, password, camera_url)
        VALUES(?, ?, ?)
        ''',
        (username, password, camera_url)
    )

    conn.commit()
    conn.close()

    return redirect('/login')

# =========================
# DASHBOARD
# =========================
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    # =====================
    # GET FALL STATUS
    # =====================
    ref = db.reference('/fall_status')
    data = ref.get()

    fall_status = "NORMAL"

    if data and 'status' in data:
        fall_status = data['status']

    # =====================
    # LOGIN
    # =====================
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        c.execute(
            '''
            SELECT * FROM users
            WHERE username=? AND password=?
            ''',
            (username, password)
        )

        user = c.fetchone()

        conn.close()

        if user:

            alerts = [
                "10:30 - Normal",
                "11:00 - Normal",
                "11:15 - Fall Detected"
            ]

            return render_template(
                'index.html',
                username=username,
                camera_status="ONLINE",
                fall_status=fall_status,
                alerts=alerts
            )

        else:

            return """
            <h1>Login Failed</h1>
            <a href="/login">Try Again</a>
            """

    # =====================
    # DIRECT ACCESS
    # =====================
    else:

        alerts = [
            "10:30 - Normal",
            "11:00 - Normal"
        ]

        return render_template(
            'index.html',
            username="Guest",
            camera_status="ONLINE",
            fall_status=fall_status,
            alerts=alerts
        )

# =========================
# VIDEO STREAM
# =========================
@app.route('/video')
def video():

    # demo image
    return redirect("https://picsum.photos/1200/700")

# =========================
# LOGOUT
# =========================
@app.route('/logout')
def logout():

    return redirect('/')

# =========================
# RUN APP
# =========================
if __name__ == '__main__':

    port = int(os.environ.get('PORT', 5000))

    app.run(
        host='0.0.0.0',
        port=port,
        debug=True
    )