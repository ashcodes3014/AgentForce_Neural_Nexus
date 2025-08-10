from app.firebaseConfig import fs

def get_linkedin_data(user_id: str) :
    doc_ref = fs.collection("users").document(user_id)
    doc = doc_ref.get()
        
    if doc.exists:
        data = doc.to_dict()
        return data
    return None
