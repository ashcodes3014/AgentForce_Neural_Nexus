from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

class EmbeddingGenerator:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def generate_embedding(self, text: str) -> np.ndarray:
        return self.model.encode(text)
    
    def batch_generate_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        return self.model.encode(texts)