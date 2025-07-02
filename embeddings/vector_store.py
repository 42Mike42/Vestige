# vector_store.py

import requests
import numpy as np
from typing import List, Dict

class VectorStore:
    def __init__(self, model_name='nomic-embed-text'):
        self.model_name = model_name
        self.embeddings = []
        self.metadata = []



    def embed_text(self, text: str) -> np.ndarray:
        url = 'http://localhost:11434/api/embeddings'
        payload = {
            'model': self.model_name,
            'prompt': text,
            
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()
        output = response.json()
        vector =output['embedding']
        return np.array(vector)

    def add_memory(self, text: str, metadata: Dict = None):
        embedding = self.embed_text(text)
        self.embeddings.append(embedding)
        self.metadata.append(metadata or {})

    def query(self, text: str, top_k: int = 5) -> List[Dict]:
        query_vec = self.embed_text(text)
        scores = []

        for i, vec in enumerate(self.embeddings):
            similarity = np.dot(vec, query_vec) / (
                np.linalg.norm(vec) * np.linalg.norm(query_vec)
            )
            entry = self.metadata[i].copy()
            entry['score'] = float(similarity)
            scores.append(entry)

        sorted_scores = sorted(scores, key=lambda x: x['score'], reverse=True)
        return sorted_scores[:top_k]
