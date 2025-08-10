import os
import numpy as np
import cohere
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

load_dotenv()

class MatchingService:
    def __init__(self):
        self.client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))

    def embed_batch(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for a batch of texts using Cohere."""
        if not texts:
            return np.empty((0,))  

        response = self.client.embed(
            texts=texts,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return np.array(response.embeddings, dtype=float)

    def embedding_similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """Compute cosine similarity between two embeddings."""
        return float(cosine_similarity([emb1], [emb2])[0][0])

    def semantic_keyword_match(self, resume_keywords: List[str], job_keywords: List[str]) -> float:
        """Return % of job keywords semantically matched in resume."""
        if not job_keywords:
            return 0.0

        resume_embs = self.embed_batch(resume_keywords)
        job_embs = self.embed_batch(job_keywords)

        match_flags = []
        for job_emb in job_embs:
            sims = cosine_similarity([job_emb], resume_embs)[0]
            match_flags.append(1 if np.max(sims) > 0.65 else 0)

        return sum(match_flags) / len(job_keywords)

    def identify_matching_issues(self, resume_keywords: List[str], job_keywords: List[str]) -> List[str]:
        """Return job keywords that are not semantically matched in resume."""
        if not job_keywords:
            return []

        resume_embs = self.embed_batch(resume_keywords)
        job_embs = self.embed_batch(job_keywords)

        missing_keywords = []
        for idx, job_emb in enumerate(job_embs):
            sims = cosine_similarity([job_emb], resume_embs)[0]
            if np.max(sims) <= 0.65:
                missing_keywords.append(job_keywords[idx])

        return missing_keywords
