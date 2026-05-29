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
| Input คืออะไร | กล้อง Webcam + Motion Detection |
| Component 1 | ESP32 อ่านค่าจาก sensor |
| Component 2 | Firebase Realtime Database |
| Component 3 | Flask Dashboard Web Application |
| Output คืออะไร | Dashboard แสดงสถานะ FALL DETECTED แบบ Realtime |

## Integration Map ของทีม (เขียนเป็น flow สั้น ๆ):
Camera/Webcam → AI Fall Detection (MediaPipe + OpenCV) → Firebase Realtime Database → Flask Backend → Dashboard UI (Realtime Monitoring)

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

## Demo link
Demo link:https : //nicecare-404teamnotfound.onrender.com/
Backup evidence : https://drive.google.com/drive/folders/1cLpCQ9PU3f_upouqT-Q17N-U3uF_Ho2a?usp=sharing

## Known Issues / Limitations
Known Issues / LimitationsFirebase realtime update ยังมี delay บางครั้งAI detection ยังขึ้นกับมุมกล้องและสภาพแสงHardware integration ยังไม่สมบูรณ์ระบบยังอยู่ใน prototype stage และยังไม่ได้ทดสอบกับผู้ใช้จริงจำนวนมาก

## Sprint 4 Test Plan
| หัวข้อ | คำตอบ |
| --- | --- |
| ผู้ใช้ที่จะทดสอบ | นักศึกษาและผู้ใช้งานทั่วไป 3–4 คน |
| Task ที่ให้ลองทำ | ทดลองจำลองการล้มหน้ากล้อง |
| สิ่งที่จะสังเกต | Dashboard แจ้งเตือนถูกต้องหรือไม่ |
| วิธีเก็บ feedback | Observation และสัมภาษณ์ |
| ตัวชี้วัดเบื้องต้น | ความแม่นยำและความเข้าใจของผู้ใช้ |
| สิ่งที่ต้องเตรียมก่อน Test | ปรับปรุงความเสถียรของ AI และ Dashboard |

## Build Log
| รายการ | คำตอบ |
| --- | --- |
| สิ่งที่ทำเสร็จจริง 3 อันดับแรก | 1. AI Fall Detection ด้วย MediaPipe + OpenCV 2) เชื่อม Firebase Realtime Database 3) Dashboard แสดงสถานะ “FALL DETECTED” |
| สิ่งที่ยังไม่เสร็จ | Hardware integration และ notification system |
| สิ่งที่ตัดออกจาก Sprint 3 | Multiple camera support และ UI enhancement บางส่วน |
| สิ่งที่ใช้ workaround | Auto refresh และ localhost demo |
| blocker สำคัญที่เจอ | Firebase delay และ AI detection ยังไม่เสถียรบางมุม |
| วิธีแก้หรือแผนรับมือ | เตรียม video backup และ mock data |
