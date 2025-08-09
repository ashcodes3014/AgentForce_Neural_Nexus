from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from tempfile import NamedTemporaryFile
from app.schema import ResumeAnalysisRequest, AnalysisResult
from app.services.document_processing import extract_text_from_pdf, process_resume_text
from app.services.embeddings import EmbeddingGenerator
from app.llm_services import LLMService
from app.services.matching import MatchingService
from app.services.storage import FirebaseService

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

@app.post("/analyze-resume/")
async def analyze_resume(file: UploadFile = File(...),job_title: str = "",user_id: str = "") -> AnalysisResult:
    try:
        # 1. Save uploaded PDF temporarily and process it
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(await file.read())
            temp_pdf_path = temp_pdf.name
        
        resume_text = extract_text_from_pdf(temp_pdf_path)
        os.unlink(temp_pdf_path)  # Delete temp file
        
        # 2. Fetch LinkedIn data from Firebase
        linkedin_data = FirebaseService.get_linkedin_data(user_id)

        # Combine resume and LinkedIn data
        combined_text = resume_text
        if linkedin_data:
            if linkedin_data.summary:
                combined_text += f"\n\nLinkedIn Summary:\n{linkedin_data.summary}"
            if linkedin_data.skills:
                combined_text += f"\n\nLinkedIn Skills:\n{linkedin_data.skills}"
        
        # 3. Extract keywords and generate summaries
        resume_keywords = llm_service.extract_keywords(combined_text)
        job_desc = llm_service.generate_job_description(job_title)
        job_keywords = llm_service.extract_keywords(job_desc)
        
        # 4. Generate embeddings
        resume_embedding = embedding_generator.generate_embedding(combined_text)
        job_embedding = embedding_generator.generate_embedding(job_desc)
        
        # 5. Calculate similarity and matching scores
        similarity_score = matching_service.calculate_similarity(resume_embedding, job_embedding)
        keyword_match_score = matching_service.keyword_match_score(resume_keywords, job_keywords)
        matching_issues = matching_service.identify_matching_issues(resume_keywords, job_keywords)
        
        # 6. Generate suggestions
        suggestions = llm_service.generate_suggestions(combined_text, job_desc, matching_issues)
        
        # 7. Generate cover letter
        cover_letter = llm_service.generate_cover_letter(combined_text, job_title, job_desc)
        
        return AnalysisResult(
            similarity_score=similarity_score,
            keyword_match_score=keyword_match_score,
            suggestions=suggestions,
            cover_letter=cover_letter
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Resume Analyzer API"}