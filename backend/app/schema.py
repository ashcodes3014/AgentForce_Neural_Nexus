from pydantic import BaseModel,EmailStr
from typing import Optional ,List

class ResumeAnalysisRequest(BaseModel):
    job_title: str
    user_id: str


class AnalysisResult(BaseModel):
    keyword_match_score: float
    suggestion: dict


class Recipient(BaseModel):
    user_id: str
    recipient_name: str
    recipient_title: str
    recipient_company: str
    recipient_location: str
    recipient_email: EmailStr


class OutputSchema(BaseModel):
    full_name: str
    job_title: str
    email: EmailStr
    phone: str
    location: str
    linkedin: str
    twitter: Optional[str] = ""
    recipient_name: str
    recipient_title: str
    recipient_company: str
    recipient_location: str
    recipient_email: EmailStr
    body: str
    college: Optional[str] = ""
    skills: List[str] = []
    projects: List[str] = []