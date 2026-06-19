import cv2
import mediapipe as mp
import firebase_admin
import requests
import numpy as np
import time

from datetime import datetime
from firebase_admin import credentials
from firebase_admin import db


# =========================
# IMAGE SOURCE
# เปลี่ยนจาก ESP32 IP มาดึงจาก Render แทน
# ESP32 → POST ภาพ → Render (/upload-frame)
# AI   → GET  ภาพ → Render (/video)
# =========================
RENDER_URL = "https://nice-care.onrender.com/video"  # Render จะเก็บภาพล่าสุดที่ ESP32 ส่งมา

# fallback: ถ้าอยากใช้ webcam PC แทน ให้เปลี่ยนเป็น True
USE_WEBCAM = False


# =========================
# FIREBASE
# =========================
cred = credentials.Certificate("backend/firebase_key.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(
        cred,
        {
            "databaseURL":
            "https://nice-care-4fa00-default-rtdb.asia-southeast1.firebasedatabase.app/"
        }
    )


# =========================
# MEDIAPIPE
# =========================
mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)


# =========================
# VARIABLES
# =========================
previous_diff_y = 1.0
last_status = "NORMAL"

last_firebase_update = 0
FIREBASE_COOLDOWN = 2  # seconds

# webcam fallback
cap = None
if USE_WEBCAM:
    cap = cv2.VideoCapture(0)
    print("AI STARTED (Webcam Mode)")
else:
    print("AI STARTED (Render Server Mode)")
    print(f"Pulling frames from: {RENDER_URL}")


# =========================
# LOOP
# =========================
while True:

    frame = None

    # =========================
    # GET IMAGE
    # =========================
    if USE_WEBCAM:
        # --- โหมด Webcam PC ---
        ret, frame = cap.read()
        if not ret or frame is None:
            print("WEBCAM ERROR")
            time.sleep(1)
            continue

    else:
        # --- โหมด Render Server ---
        # Render จะเก็บภาพล่าสุดที่ ESP32 ส่งมา
        # AI ดึงภาพนั้นมาวิเคราะห์
        try:
            response = requests.get(RENDER_URL, timeout=5)

            if response.status_code == 204:
                # ยังไม่มีภาพจาก ESP32 เลย
                print("Waiting for ESP32 frame...")
                time.sleep(2)
                continue

            if response.status_code != 200:
                print(f"Server error: {response.status_code}")
                time.sleep(2)
                continue

            img = np.frombuffer(response.content, np.uint8)
            frame = cv2.imdecode(img, cv2.IMREAD_COLOR)

            if frame is None:
                print("FRAME DECODE FAILED")
                time.sleep(1)
                continue

        except Exception as e:
            print("CONNECTION LOST:", e)
            time.sleep(2)
            continue


    # =========================
    # PROCESS FRAME
    # =========================
    frame = cv2.resize(frame, (960, 540))
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = pose.process(rgb)

    fall_status = "NORMAL"

    if results.pose_landmarks:

        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        shoulder = results.pose_landmarks.landmark[11]
        hip = results.pose_landmarks.landmark[23]

        diff_y = abs(shoulder.y - hip.y)
        movement_speed = abs(previous_diff_y - diff_y)

        # =========================
        # FALL DETECTION LOGIC
        # =========================
        if diff_y < 0.10 and movement_speed > 0.05:
            fall_status = "FALL DETECTED"

        previous_diff_y = diff_y


    # =========================
    # FIREBASE (ANTI-SPAM)
    # =========================
    current_time = time.time()

    if fall_status != last_status and (current_time - last_firebase_update > FIREBASE_COOLDOWN):

        try:
            ref = db.reference("/fall_status")

            ref.set({
                "status": fall_status,
                "time": datetime.now().strftime("%H:%M:%S")
            })

            print("SEND →", fall_status)

            last_status = fall_status
            last_firebase_update = current_time

        except Exception as e:
            print("FIREBASE ERROR:", e)


    # =========================
    # UI
    # =========================
    color = (0, 255, 0) if fall_status == "NORMAL" else (0, 0, 255)

    cv2.putText(
        frame,
        fall_status,
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color,
        3
    )

    # แสดง source ที่กำลังใช้
    source_label = "Webcam" if USE_WEBCAM else "ESP32 via Render"
    cv2.putText(
        frame,
        f"Source: {source_label}",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (200, 200, 200),
        1
    )

    cv2.imshow("NiceCare AI", frame)

    if cv2.waitKey(1) == 27:
        break


# =========================
# CLEANUP
# =========================
if cap:
    cap.release()
cv2.destroyAllWindows()