from langchain_cohere import CohereEmbeddings
import numpy as np
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class EmbeddingGenerator:
    def __init__(self):
        self.client = CohereEmbeddings(
            model="embed-english-v3.0",
            cohere_api_key=os.getenv("COHERE_API_KEY"),
        )
    
    def generate_embedding(self, text: str) -> np.ndarray:
        response = self.client.embed_query(texts=[text], input_type="search_document")
        return np.array(response.embeddings[0])
    
    def batch_generate_embeddings(self, texts: List[str]) -> List[np.ndarray]:
        response = self.client.embed(texts=texts,input_type="search_document")
        return [np.array(embedding) for embedding in response.embeddings]