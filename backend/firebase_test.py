import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("Backend/firebase_key.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://nice-care-4fa00-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref = db.reference('/fall_status')

ref.set({
    'status': 'TEST'
})

print("Firebase Connected!")