from __future__ import annotations
import streamlit as st

from src.retrieve import Retriever
from src.hybrid_router import route_query
from src.answer_engine import build_grounded_answer

st.set_page_config(page_title="Enterprise RAG AI Platform", layout="wide")
st.title("Enterprise RAG AI Platform")
st.caption("Hybrid retrieval over SQL-derived business context and business policy documents.")

@st.cache_resource
def get_retriever():
    return Retriever()

retriever = get_retriever()
query = st.text_input("Ask a question", value="Which customers are high value and what support policy applies to them?")

if st.button("Search"):
    mode = route_query(query)
    source_filter = None if mode == "hybrid" else mode
    results = retriever.search(query, top_k=6, source_filter=source_filter)
    st.subheader(f"Routing mode: {mode}")
    st.text(build_grounded_answer(query, results))
    st.subheader("Retrieved context")
    for item in results:
        st.markdown(f"**Source:** {item.get('source_type')} | **Label:** {item.get('table') or item.get('file_name') or item.get('id')}")
        st.write(item["text"])
        st.caption(f"Score: {item['score']:.4f}")