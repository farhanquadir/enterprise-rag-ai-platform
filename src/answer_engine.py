def build_grounded_answer(query: str, retrieved):
    if not retrieved:
        return 'I could not find enough relevant context to answer that question.'
    lines = [f'Question: {query}', '', 'Grounded answer:']
    for item in retrieved[:5]:
        label = item.get('table') or item.get('file_name') or item.get('id', 'source')
        lines.append(f"- [{item.get('source_type', 'unknown')}] {label}: {item['text']}")
    lines.append('')
    lines.append('Synthesis:')
    lines.append(' '.join(item['text'] for item in retrieved[:4])[:1200])
    return '\n'.join(lines)
