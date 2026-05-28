## Blocker ตอนนี้

Blocker คือปัญหาที่เกิดขึ้นแล้วและทำให้งานไปต่อไม่ได้

| Blocker | กระทบ component ใด | ใครรับผิดชอบ | ลองแก้แล้วอย่างไร | ต้องการให้ใครช่วย |
| --- | --- | --- | --- | --- |
| Dashboard แสดง NORMAL ตลอด | Flask Dashboard | สรวิชญ์ | แก้ logic fall detection และเพิ่ม cooldown | - |
| Dashboard ยังไม่ realtime | Dashboard | ทิพย์อาภา | ทดลอง subscribe topic | - |

## Risk ที่คาดว่าจะเจอใน Sprint 3

Risk คือสิ่งที่ยังไม่เกิด แต่อาจทำให้ Sprint ไม่สำเร็จ
| Risk | โอกาสเกิด ต่ำ/กลาง/สูง | ผลกระทบ ต่ำ/กลาง/สูง | แผนรับมือ / Fallback |
| --- | --- | --- | --- |
| ESP32 disconnect | สูง | สูง | เตรียม video backup |
| AI detect ไม่เสถียร | กลาง | สูง | อัดวิดีโอสำรองตอนระบบทำงานได้ |
