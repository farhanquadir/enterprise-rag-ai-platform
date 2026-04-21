SQL_HINTS = {'customer', 'customers', 'country', 'revenue', 'invoice', 'sales', 'monthly', 'trend', 'value'}
DOC_HINTS = {'policy', 'program', 'escalation', 'guide', 'memo', 'refund', 'support', 'loyalty'}

def route_query(query: str) -> str:
    tokens = set(query.lower().split())
    sql_hits = len(tokens & SQL_HINTS)
    doc_hits = len(tokens & DOC_HINTS)
    if sql_hits > doc_hits:
        return 'sql'
    if doc_hits > sql_hits:
        return 'doc'
    return 'hybrid'
