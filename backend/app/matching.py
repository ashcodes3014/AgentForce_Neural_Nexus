import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

class MatchingService:
    def __init__(self):
        pass
    
    def calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        return cosine_similarity([embedding1], [embedding2])[0][0]
    
    def keyword_match_score(self, resume_keywords: List[str], job_keywords: List[str]) -> float:
        matched = set(resume_keywords) & set(job_keywords)
        return len(matched) / len(job_keywords) if job_keywords else 0
    
    def identify_matching_issues(self, resume_keywords: List[str], job_keywords: List[str]) -> List[str]:
        missing_keywords = set(job_keywords) - set(resume_keywords)
        return list(missing_keywords)