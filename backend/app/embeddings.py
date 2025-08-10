import cohere
import numpy as np
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

class EmbeddingGenerator:
    def __init__(self):
        self.client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))
    
    def generate_embedding(self, text: str) -> np.ndarray:
        response = self.client.embed(
            texts=[text],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return np.array(response.embeddings[0])
    
    def batch_generate_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        response = self.client.embed(
            texts=texts,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return [np.array(e) for e in response.embeddings]
