# NiceCare_404TeamNotFound

# Team Members

| ชื่อสมาชิก | Role |
| --- | --- |
| กรัณย์ชมพู วงษ์เสถียร | Project Manager / Product |
| วชิราภรณ์ สอนวงศ์ษา | Project Manager / Scrum Lead |
| สรวิชญ์ คูหะมณี | Data / AI Developer |
| ทิพย์อาภา จริยวงศ์พรหม | Embedded / IoT Developer |

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
