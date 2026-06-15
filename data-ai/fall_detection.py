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
# ESP32 CAMERA
# =========================
ESP32_URL = "http://10.194.23.33/capture"


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
# FALL VARIABLES
# =========================
previous_diff_y = 1.0
last_status = "NORMAL"

last_fall_time = 0
fall_detected_until = 0


print("AI STARTED")


# =========================
# LOOP
# =========================
while True:

    try:

        response = requests.get(
            ESP32_URL,
            timeout=1
        )

        img = np.frombuffer(
            response.content,
            np.uint8
        )

        frame = cv2.imdecode(
            img,
            cv2.IMREAD_COLOR
        )

        if frame is None:
            continue

    except:

        print("ESP32 LOST")

        continue


    frame = cv2.resize(
        frame,
        (960, 540)
    )

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

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

        diff_y = abs(
            shoulder.y - hip.y
        )

        movement_speed = abs(
            previous_diff_y - diff_y
        )

        current = time.time()


        if diff_y < 0.10 and movement_speed > 0.05:

            if current - last_fall_time > 5:

                fall_detected_until = current + 5

                last_fall_time = current


        if current < fall_detected_until:

            fall_status = "FALL DETECTED"

        previous_diff_y = diff_y


    if fall_status != last_status:

        ref = db.reference(
            "/fall_status"
        )

        ref.set({

            "status":
            fall_status,

            "time":
            datetime.now().strftime(
                "%H:%M:%S"
            )

        })

        print(
            "SEND →",
            fall_status
        )

        last_status = fall_status


    color = (
        (0,255,0)
        if fall_status=="NORMAL"
        else
        (0,0,255)
    )

    cv2.putText(

        frame,

        fall_status,

        (20,50),

        cv2.FONT_HERSHEY_SIMPLEX,

        1,

        color,

        3
    )


    cv2.imshow(
        "NiceCare AI",
        frame
    )


    if cv2.waitKey(1)==27:
        break


cv2.destroyAllWindows()