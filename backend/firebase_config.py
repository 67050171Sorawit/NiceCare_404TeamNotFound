import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# โหลด Firebase Key
cred = credentials.Certificate("firebase_key.json")

# เชื่อม Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://nice-care-4fa00-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

# =========================
# STATUS CONNECT
# =========================
ref = db.reference('/')

ref.set({
    'status': 'NiceCare Connected'
})

# =========================
# FALL STATUS
# =========================
fall_ref = db.reference('/fall_status')

fall_ref.set({
    'status': 'NORMAL'
})

print("Firebase Connected!")
print("Fall Status Updated!")