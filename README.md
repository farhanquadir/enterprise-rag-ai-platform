# 🚀 Enterprise RAG AI Platform  
A portfolio project demonstrating *A Hybrid Retrieval-Augmented Generation System over Structured + Unstructured Data*

---

## 📌 Overview

This project implements an **enterprise-grade Retrieval-Augmented Generation (RAG) platform** that integrates:

- 📊 Structured analytics data (SQL warehouse)  
- 📄 Unstructured business documents (policies, guides)  
- 🤖 LLM-based reasoning with hybrid routing  

---
## Skills Demonstrated

- Retrieval-Augmented Generation (RAG)
- Embeddings
- Vector Search
- FAISS
- Structured-to-Text Transformation
- Grounded Answer Generation
- Hybrid Retrieval
- AI System Design

## 🧠 Key Capabilities

### 🔍 Hybrid Retrieval
- SQL-based retrieval from analytics warehouse tables  
- Semantic document retrieval using embeddings + FAISS  
- Intelligent query routing:  
  - `sql` → structured data  
  - `doc` → documents  
  - `hybrid` → both  

### 🧾 Grounded Responses
Each answer includes:
- Source attribution (`[sql]`, `[doc]`)  
- Evidence-backed reasoning  
- Final synthesized answer  

---

## 🏗️ Architecture

```
User Question → Router → (SQL + Docs) → LLM → Answer
```

---

## 📊 Data Sources

### Structured Tables
- `fct_order_lines`
- `dim_customers`, `dim_products`, `dim_dates`
- `mart_monthly_revenue`
- `mart_country_sales`
- `mart_top_customers`
- `ai_customer_context`

### Documents
- `support_escalation.txt`
- `loyalty_program.txt`

---

## ⚙️ Pipeline Workflow

### 1. Extract SQL Context
```bash
python src/extract_sql_context.py
```

### 2. Build Index
```bash
python src/build_index.py
```

### 3. Query System
```bash
python src/query_rag.py
```

---

## 🧪 Example Queries

- Which customers are high value?  
- Which countries generate the most revenue?  
- What does the loyalty program say about premium customers?  

---

## 🧠 Routing Logic

| Query Type | Route |
|-----------|------|
| Aggregations | SQL |
| Policies | Docs |
| Business reasoning | Hybrid |

---

## 📁 Project Structure

```
enterprise-rag-ai-platform/
│
├── data/
│   ├── warehouse.db
│   ├── docs/
│   └── exports/
│
├── src/
│   ├── config.py
│   ├── extract_sql_context.py
│   ├── ingest_documents.py
│   ├── build_index.py
│   ├── query_rag.py
│
├── scripts/
│   └── export_analytics.py
│
├── notebooks/
│
└── README.md
```

---

## 🚀 Run in Google Colab

```python
from google.colab import drive
drive.mount('/content/drive')
```

```bash
cd /content/drive/MyDrive/projects/enterprise-rag-ai-platform
```

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
python src/extract_sql_context.py
python src/build_index.py
python src/query_rag.py
```

---

## ⚠️ Common Issues

### ModuleNotFoundError: src
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

---

## 📈 Future Improvements

- Replace FAISS with Pinecone / Weaviate  
- Add LangChain / LlamaIndex orchestration  
- Deploy UI (Streamlit / React)  
- Add logging, monitoring, and access control  
- Production deployment
- Authentication
- Monitoring
- LLM evaluation frameworks
- Cloud infrastructure
---

## 👩‍💻 Author

**Farhan Quadir**  
Postdoctoral Researcher, University of Chicago  

---

## ⭐ Summary

This project demonstrates:

✔ Hybrid AI system (data + documents)  
✔ Explainable, grounded LLM outputs  
✔ Real-world enterprise analytics integration  
