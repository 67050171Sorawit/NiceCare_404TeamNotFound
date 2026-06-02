## Prototype v1 Readiness Check
| รายการ | สถานะ | หลักฐาน / Link |
| --- | --- | --- |
| Prototype เปิดดูหรือทดลองได้ | Partly Ready | รันระบบแบบ Local (Flask + OpenCV Webcam) และเชื่อม Firebase |
| Core Flow หลักยังอยู่ครบ | Ready | กล้องตรวจจับการล้ม —> อัปเดตขึ้น Firebase —>Dashboard เปลี่ยนสถานะ |
| มี demo link / file / device / Figma / notebook | Ready | **https://drive.google.com/drive/folders/1cLpCQ9PU3f_upouqT-Q17N-U3uF_Ho2a?usp=sharing** |
| มี known issues ที่ทีมรู้อยู่แล้ว | มี | ระบบยังมีอาการ Delay ในการดึงค่าจาก Firebase ประมาณ 3-5 วินาทีในบางช่วง |
| มี workaround ถ้าระบบพัง | มี |  ใช้ Demo Video, Mock Firebase Data และ Local Dashboard แทนระบบออนไลน์ |
| ผู้ใช้สามารถลอง task ได้โดยไม่ต้องอธิบายยาว | Partly Ready | หน้าเว็บเข้าใจง่าย แต่ต้องให้ผู้ใช้อยู่ในจุดที่กล้องจับภาพได้พอดี |

## Prototype v1 ที่จะใช้ทดสอบ
| รายการ | คำตอบ |
| --- | --- |
| Prototype ที่ใช้ทดสอบคืออะไร | เว็บแอปพลิเคชัน NiceCare (Flask Backend) ทำงานร่วมกับระบบ AI Pose Estimation (MediaPipe) ผ่านกล้อง Webcam และระบบ Firebase Realtime Database |
| Link / File / Device / Location | **https://drive.google.com/drive/folders/1cLpCQ9PU3f_upouqT-Q17N-U3uF_Ho2a?usp=sharing** |
| Core Flow ที่จะทดสอบ | ผู้ดูแลรับรู้สถานะการล้มของผู้สูงอายุผ่านหน้าจอ Dashboard หลังจาก AI ตรวจจับพฤติกรรมจากกล้องแล้วส่งข้อมูลเรียลไทม์ |
| สิ่งที่ prototype ทำได้แล้ว | AI ตรวจจับการล้มได้จริง, ซิงก์ค่าขึ้น Cloud ได้, และหน้า Dashboard แสดงผลข้อความแจ้งเตือน "FALL DETECTED" พร้อมแถบสีแดงเตือนภัย |
| ข้อจำกัดที่ต้องบอกผู้ใช้ก่อน test | ระบบรันแบบ Local บนเครื่องเครื่องหลัก และอาจมี Delay ในการส่งข้อมูลผ่านอินเทอร์เน็ตเล็กน้อย |
