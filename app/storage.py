from app.models.firebase import init_firebase
from app.models.schemas import LinkedInProfile
from typing import Optional

db = init_firebase()

class FirebaseService:
    @staticmethod
    def get_linkedin_data(user_id: str) -> Optional[LinkedInProfile]:
        doc_ref = db.collection("users").document(user_id).collection("profiles").document("linkedin")
        doc = doc_ref.get()
        
        if doc.exists:
            data = doc.to_dict()
            return LinkedInProfile(
                summary=data.get("summary"),
                experiences=data.get("experiences"),
                skills=data.get("skills"),
                education=data.get("education")
            )
        return None