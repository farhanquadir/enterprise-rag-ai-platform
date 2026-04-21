from src.retrieve import Retriever
from src.hybrid_router import route_query
from src.answer_engine import build_grounded_answer

QUERIES = [
    'Which customers are high value and what support policy applies to them?',
    'What does the loyalty program say about premium customers?',
    'Which countries generate the most revenue?',
    'Summarize the monthly revenue trend and the sales strategy.'
]

def main():
    retriever = Retriever()
    for query in QUERIES:
        mode = route_query(query)
        source_filter = None if mode == 'hybrid' else mode
        results = retriever.search(query, top_k=6, source_filter=source_filter)
        print('=' * 90)
        print('Routing mode:', mode)
        print(build_grounded_answer(query, results))
        print()

if __name__ == '__main__':
    main()
