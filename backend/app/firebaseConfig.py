import firebase_admin
from firebase_admin import firestore, credentials
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(BASE_DIR, "firebase.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://defi-ai-assistant-default-rtdb.firebaseio.com/"
    })

fs = firestore.client()