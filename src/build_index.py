from __future__ import annotations
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

from src.config import EMBEDDING_MODEL, EXPORTS_DIR, VECTORSTORE_DIR
from src.utils import ensure_dir, load_pickle, save_pickle

def main() -> None:
    sql_records = load_pickle(EXPORTS_DIR / 'sql_context.pkl')
    doc_records = load_pickle(EXPORTS_DIR / 'doc_chunks.pkl')
    records = sql_records + doc_records
    if not records:
        raise ValueError('No records found for indexing.')

    model = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = model.encode([r['text'] for r in records], normalize_embeddings=True, show_progress_bar=True)
    embeddings = np.asarray(embeddings, dtype='float32')

    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    ensure_dir(VECTORSTORE_DIR)
    faiss.write_index(index, str(VECTORSTORE_DIR / 'faiss.index'))
    save_pickle(records, VECTORSTORE_DIR / 'metadata.pkl')
    print(f'Built FAISS index with {len(records)} records')

if __name__ == '__main__':
    main()
