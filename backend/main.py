from fastapi import FastAPI, UploadFile, File ,Form,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime
from tempfile import NamedTemporaryFile
from app.schema import AnalysisResult ,Recipient,OutputSchema
from app.document_processing import extract_text_from_pdf
from app.embeddings import EmbeddingGenerator
from app.model import Filtering
from app.llm_services import LLMService
from app.matching import MatchingService
from app.storage import get_linkedin_data
from app.firebaseConfig import fs
from firebase_admin import firestore
from app.storage import arr

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

embedding_generator = EmbeddingGenerator()
llm_service = LLMService()
matching_service = MatchingService()
filters = Filtering()

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...),job_title: str = Form(...),user_id: str = Form("")) -> AnalysisResult :
    try:
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(await file.read())
            temp_pdf_path = temp_pdf.name
        
        text = extract_text_from_pdf(temp_pdf_path)
        os.unlink(temp_pdf_path)
         
        resume_text = filters.extract_text(text=text)
        linkedin_data = filters.extract_text_from_object(get_linkedin_data(user_id))

        combined_text = filters.merge_duplicates(resume_text,linkedin_data)
        
        resume_keywords = llm_service.extract_keywords(combined_text)
        job_desc = llm_service.generate_job_description(job_title)
        job_keywords = llm_service.extract_keywords_for_job(job_title)

        keyword_match_score = matching_service.semantic_keyword_match(resume_keywords, job_keywords)
        matching_issues = matching_service.identify_matching_issues(resume_keywords, job_keywords)
        
        suggestions = llm_service.generate_suggestions(combined_text, job_desc, matching_issues)

        history_item = {
            "resume_summary": combined_text,
            "job_title": job_title,
            "job_desc": job_desc,
            "created_at": datetime.utcnow(),
            "keyword_match_score":keyword_match_score,
            "suggestion":suggestions
        }


        if arr[1].exists and "history" in arr[1].to_dict():
            arr[0].update({
                "history": firestore.ArrayUnion([history_item])
            })
        else:
            arr[0].set({
                "history": [history_item]
            }, merge=True)

        
        return AnalysisResult(
            keyword_match_score=keyword_match_score,
            suggestion = suggestions,
        )
        
    except Exception as e:
        print(f"error : {e}")

@app.post("/coverLetter/", response_model=OutputSchema)
async def create_recipient(r: Recipient):
    try:
        user_ref = fs.collection('users').document(r.user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="User not found")
            
        user_data = user_doc.to_dict()
        
        if "history" not in user_data or not user_data["history"]:
            raise HTTPException(status_code=400, detail="No resume history found for this user")
            
        latest_history = user_data["history"][-1]
        
        cover_letter = llm_service.generate_cover_letter(
            resume_summary=latest_history["resume_summary"],
            job_title=latest_history["job_title"],
            job_desc=latest_history["job_desc"],
            recipient_name=r.recipient_name,
            recipient_title=r.recipient_title,
            recipient_company=r.recipient_company,
            recipient_location=r.recipient_location,
            recipient_email=r.recipient_email
        )
        
        return OutputSchema(**cover_letter)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"error : {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def read_root():
    return {"message": "Resume Analyzer API"}