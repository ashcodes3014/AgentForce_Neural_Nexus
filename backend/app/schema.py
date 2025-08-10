from pydantic import BaseModel

class ResumeAnalysisRequest(BaseModel):
    job_title: str
    user_id: str


class AnalysisResult(BaseModel):
    similarity_score: float
    keyword_match_score: float
    suggestion: list[str]
    cover_letter: str