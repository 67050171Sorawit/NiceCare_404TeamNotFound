import cv2
import mediapipe as mp
import firebase_admin
import time

from datetime import datetime
from firebase_admin import credentials
from firebase_admin import db

# =========================
# FIREBASE
# =========================

cred = credentials.Certificate("backend/firebase_key.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://nice-care-4fa00-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# =========================
# MEDIAPIPE SETUP
# =========================

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

pose = mp_pose.Pose()

# =========================
# CAMERA
# =========================

cap = cv2.VideoCapture(0)

# =========================
# FALL VARIABLES
# =========================

previous_diff_y = 1.0
last_status = "NORMAL"
last_fall_time = 0
fall_detected_until = 0

# =========================
# MAIN LOOP
# =========================

while True:

    success, frame = cap.read()

    if not success:
        break

    # mirror
    frame = cv2.flip(frame, 1)

    # BGR -> RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # AI PROCESS
    results = pose.process(rgb)

    fall_status = "NORMAL"

    # DRAW SKELETON
    if results.pose_landmarks:

        mp_draw.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        # =========================
        # FALL DETECTION
        # =========================

        shoulder = results.pose_landmarks.landmark[11]
        hip = results.pose_landmarks.landmark[23]

        diff_y = abs(shoulder.y - hip.y)

        # movement speed
        movement_speed = abs(previous_diff_y - diff_y)

        current_time = time.time()

        # FALL LOGIC
        if diff_y < 0.1 and movement_speed > 0.05:

            # cooldown 5 sec
            if current_time - last_fall_time > 5:

                fall_detected_until = current_time + 5
                last_fall_time = current_time

        # keep FALL DETECTED for 5 sec
        if current_time < fall_detected_until:
            fall_status = "FALL DETECTED"
        else:
            fall_status = "NORMAL"

        previous_diff_y = diff_y

        # =========================
        # SEND TO FIREBASE
        # =========================

        if fall_status != last_status:

            ref = db.reference('/fall_status')

            ref.set({
                'status': fall_status,
                'time': datetime.now().strftime("%H:%M:%S")
            })

            print("SEND:", fall_status)

            last_status = fall_status

        # =========================
        # SHOW STATUS
        # =========================

        color = (0, 255, 0)

        if fall_status == "FALL DETECTED":
            color = (0, 0, 255)

        cv2.putText(
            frame,
            fall_status,
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            3
        )

    # SHOW
    cv2.imshow("NiceCare AI Fall Detection", frame)

    # PRESS Q TO EXIT
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()