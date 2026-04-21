from __future__ import annotations
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from src.config import EMBEDDING_MODEL, VECTORSTORE_DIR, TOP_K
from src.utils import load_pickle

class Retriever:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.index = faiss.read_index(str(VECTORSTORE_DIR / 'faiss.index'))
        self.metadata = load_pickle(VECTORSTORE_DIR / 'metadata.pkl')

    def search(self, query: str, top_k: int = TOP_K, source_filter: str | None = None):
        q = self.model.encode([query], normalize_embeddings=True)
        q = np.asarray(q, dtype='float32')
        scores, idxs = self.index.search(q, min(top_k * 3, len(self.metadata)))
        results = []
        for score, idx in zip(scores[0], idxs[0]):
            if idx < 0:
                continue
            item = dict(self.metadata[idx])
            item['score'] = float(score)
            if source_filter and item.get('source_type') != source_filter:
                continue
            results.append(item)
            if len(results) >= top_k:
                break
        return results
