from pydantic import BaseModel
from typing import Optional

class ResumeAnalysisRequest(BaseModel):
    job_title: str
    user_id: str

class LinkedInProfile(BaseModel):
    summary: Optional[str] = None
    experiences: Optional[str] = None
    skills: Optional[str] = None
    education: Optional[str] = None

class AnalysisResult(BaseModel):
    similarity_score: float
    keyword_match_score: float
    suggestions: list[str]
    cover_letter: str