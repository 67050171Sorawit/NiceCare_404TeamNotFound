import cv2
import numpy as np
import requests
import mediapipe as mp

url = "http://10.194.23.33/capture"  # เปลี่ยน IP

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

while True:
    img_resp = requests.get(url, timeout=5)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    frame = cv2.imdecode(img_arr, -1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        lm = results.pose_landmarks.landmark

        shoulder_y = lm[mp_pose.PoseLandmark.LEFT_SHOULDER].y
        hip_y = lm[mp_pose.PoseLandmark.LEFT_HIP].y

        # 🔥 logic ตรวจล้มแบบง่าย
        if abs(shoulder_y - hip_y) < 0.1:
            cv2.putText(frame, "⚠ FALL RISK", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            print("⚠ Possible Fall Detected")

    cv2.imshow("ESP32-CAM AI", frame)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()