from app.firebaseConfig import fs
from typing import Optional


def get_linkedin_data(user_id: str) :
    doc_ref = fs.collection("users").document(user_id)
    doc = doc_ref.get()
        
    if doc.exists:
        data = doc.to_dict()
        return data
    return None


# print(get_linkedin_data("test_user"))