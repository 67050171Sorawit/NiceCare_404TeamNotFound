import cv2
import mediapipe as mp

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# =========================
# FIREBASE
# =========================

cred = credentials.Certificate("firebase_key.json")

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

        # ถ้าลำตัวแนวนอนเกินไป
        if diff_y < 0.1:
            fall_status = "FALL DETECTED"

        # =========================
        # SEND TO FIREBASE
        # =========================

        ref = db.reference('/fall_status')

        ref.set({
            'status': fall_status
        })

        # =========================
        # SHOW STATUS
        # =========================

        cv2.putText(
            frame,
            fall_status,
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

    # SHOW
    cv2.imshow("NiceCare AI Fall Detection", frame)

    # PRESS Q TO EXIT
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()