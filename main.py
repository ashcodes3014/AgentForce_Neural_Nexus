from fastapi import FastAPI, UploadFile, File ,Form
from fastapi.middleware.cors import CORSMiddleware
import os
from tempfile import NamedTemporaryFile
from app.schema import AnalysisResult
from app.document_processing import extract_text_from_pdf
from app.embeddings import EmbeddingGenerator
from app.model import Filtering
from app.llm_services import LLMService
from app.matching import MatchingService
from app.storage import get_linkedin_data

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
async def analyze_resume(file: UploadFile = File(...),job_title: str = Form(...),user_id: str = Form("")) -> AnalysisResult:
    try:
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(await file.read())
            temp_pdf_path = temp_pdf.name
        
        text = extract_text_from_pdf(temp_pdf_path)
        os.unlink(temp_pdf_path)
        resume_text = filters.extract_text(text=text)

         
        linkedin_data = get_linkedin_data(user_id)
        linkedin_data = filters.extract_text_from_object(get_linkedin_data(user_id))

        print(linkedin_data)

        combined_text = resume_text
        if linkedin_data:
            combined_text = resume_text+linkedin_data

        
        resume_keywords = llm_service.extract_keywords(combined_text)
        job_desc = llm_service.generate_job_description(job_title)
        job_keywords = llm_service.extract_keywords(job_desc)
        resume_embedding = embedding_generator.generate_embedding(combined_text)


        job_embedding = embedding_generator.generate_embedding(job_desc)
        
        similarity_score = matching_service.calculate_similarity(resume_embedding, job_embedding)
        keyword_match_score = matching_service.keyword_match_score(resume_keywords, job_keywords)
        matching_issues = matching_service.identify_matching_issues(resume_keywords, job_keywords)
        
        suggestions = llm_service.generate_suggestions(combined_text, job_desc, matching_issues)
        cover_letter = llm_service.generate_cover_letter(combined_text, job_title, job_desc)
        
        return AnalysisResult(
            similarity_score=similarity_score,
            keyword_match_score=keyword_match_score,
            suggestion = suggestions,
            cover_letter=cover_letter
        )
        
    except Exception as e:
        print(f"error : {e}")

@app.get("/")
def read_root():
    return {"message": "Resume Analyzer API"}