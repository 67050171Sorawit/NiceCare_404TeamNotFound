# NiceCare_404TeamNotFound

# Team Members

| ชื่อสมาชิก | Role |
| --- | --- |
| กรัณย์ชมพู วงษ์เสถียร | Project Manager / Product |
| วชิราภรณ์ สอนวงศ์ษา | Project Manager / Scrum Lead |
| สรวิชญ์ คูหะมณี | Data / AI Developer |
| ทิพย์อาภา จริยวงศ์พรหม | Embedded / IoT Developer |

## Integration Map (แผนภาพการเชื่อมระบบ)
| ส่วน | คำตอบของทีม |
| --- | --- |
| Input คืออะไร | Motion Sensor / Push Button |
| Component 1 | ESP32 อ่านค่าจาก sensor |
| Component 2 | micro-ROS Publisher ส่งข้อมูลเข้า ROS2 Topic |
| Component 3 | ROS2 Subscriber รับค่าและแสดงผล |
| Output คืออะไร | Serial Monitor / Dashboard แสดงสถานะ |

## Integration Map ของทีม (เขียนเป็น flow สั้น ๆ):
Motion Sensor → ESP32 → micro-ROS Publisher → ROS2 Topic (/motion_status) → Subscriber Node → Serial Monitor / Dashboard

## Scope Cut Table

| Must Finish for Demo | Can Demo with Workaround | Cut for Sprint 3 |
| --- | --- | --- |
| Dashboard สำหรับดูสถานะ  |  ถ้า deploy มีปัญหา ใช้ localhost demo ในเครื่องแทน | Multiple Camera Support |
| ระบบตรวจจับการล้มด้วย AI | ถ้า realtime มีปัญหา ใช้ auto refresh หน้าเว็บแทน | ระบบแจ้งเตือน (Notification) |

## NiceCare Prototype v1 — Current Capabilities
ระบบตอนนี้ทำอะไรได้บ้าง
1. AI Pose Detection
ใช้ MediaPipe ตรวจจับร่างกายจาก webcam แสดง skeleton / pose landmarks แบบ realtime
2. Fall Detection Logic
วิเคราะห์ตำแหน่งไหล่และสะโพก ตรวจจับการเปลี่ยนท่าทางที่คล้ายการล้ม
เปลี่ยนสถานะเป็น:
NORMAL
FALL DETECTED
3. Firebase Realtime Update
ส่งสถานะการล้มเข้า Firebase Realtime Database อัปเดตข้อมูลแบบ realtime
4. Flask Backend
มี backend API ด้วย Flask Deploy backend บน Render ได้
5. Core Flow Integration
ระบบสามารถทำ flow หลักได้ดังนี้:
Camera
→ AI Pose Detection
→ Fall Detection
→ Firebase Update
→ Dashboard / Backend
6. Demo Prototype
สามารถ demo การตรวจจับการล้มได้ แสดง realtime status ได้
