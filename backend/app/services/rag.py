from uuid import uuid4
from app.services.qdrant_client import get_qdrant
from app.services.doc_processing import extract_text, clean_text, chunk_text, chunk_text_with_pages
from app.services.embeddings import embed_texts
from app.config import GROQ_API_KEY, GROQ_MODEL
import requests
import json


def index_document(filename: str, data: bytes, metadata: dict):
    text, page_map = extract_text(filename, data)
    text = clean_text(text)
    if not text:
        return {"error": "No extractable text"}

    # Preserve page numbers for citations
    if page_map:
        chunk_items = chunk_text_with_pages(page_map)
        chunks = [c['text'] for c in chunk_items]
    else:
        chunks = chunk_text(text)
        chunk_items = [{"text": c, "page": None} for c in chunks]

    vectors = embed_texts(chunks)
    q = get_qdrant()
    q._ensure_collection(vector_size=len(vectors[0]))

    payloads = []
    for chunk, meta in zip(chunk_items, [metadata]*len(chunk_items)):
        payloads.append({
            "id": str(uuid4()),
            "text": chunk['text'],
            "page": chunk.get('page'),
            **meta
        })

    q.upsert(vectors, payloads)
    return {"message": "Indexed", "chunks": len(chunks)}


def groq_chat(prompt: str):
    if not GROQ_API_KEY:
        return "Groq API key not configured. Set GROQ_API_KEY in .env."
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are PlacementIQ. Answer concisely with high-signal placement prep guidance."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


def groq_chat_stream(prompt: str):
    if not GROQ_API_KEY:
        yield "Groq API key not configured. Set GROQ_API_KEY in .env."
        return
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are PlacementIQ. Answer concisely with high-signal placement prep guidance."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "stream": True
    }
    with requests.post(url, json=payload, headers=headers, stream=True, timeout=60) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if not line:
                continue
            if line.startswith(b'data: '):
                data = line[len(b'data: '):]
                if data == b'[DONE]':
                    break
                try:
                    j = json.loads(data.decode())
                    delta = j["choices"][0]["delta"].get("content")
                    if delta:
                        yield delta
                except Exception:
                    continue


def _extract_query_terms(question: str):
    """Pull out company/topic keywords from the query."""
    q = question.lower()
    # Known companies
    companies = ['tcs', 'infosys', 'wipro', 'capgemini', 'accenture', 'cts', 'cognizant',
                 'amazon', 'google', 'microsoft', 'meta', 'netflix', 'adobe', 'salesforce',
                 'mindtree', 'tech mahindra', 'hcl', 'ibm', 'oracle', 'sap']
    topics = ['dbms', 'sql', 'mysql', 'mongodb', 'postgres', 'database',
              'os', 'operating system', 'cn', 'computer networks', 'networking',
              'dsa', 'data structures', 'algorithms', 'oops', 'object oriented',
              'java', 'python', 'c++', 'javascript', 'coding', 'aptitude', 'logical']
    found_companies = [c for c in companies if c in q]
    found_topics = [t for t in topics if t in q]
    return set(found_companies), set(found_topics)


def _is_relevant(query: str, results):
    """Check if retrieved docs are actually relevant to the query."""
    q_companies, q_topics = _extract_query_terms(query)

    if not q_companies and not q_topics:
        return True  # Generic query, trust the retriever

    for r in results:
        p = r.payload or {}
        doc_company = (p.get('company') or '').lower()
        doc_topic = (p.get('topic') or '').lower()
        doc_round = (p.get('round_type') or '').lower()
        doc_text = (p.get('text') or '').lower()

        # If query mentions a company, doc should mention it or be from that company
        if q_companies:
            matched_company = any(c in doc_company or c in doc_topic or
                                   c in doc_round or c in doc_text
                                   for c in q_companies)
            if not matched_company:
                return False

        # If query mentions a specific topic, doc should reference it
        if q_topics:
            matched_topic = any(t in doc_topic or t in doc_text for t in q_topics)
            if not matched_topic:
                return False

    return True


def answer_question(question: str, filters: dict | None = None):
    if not question:
        return {"answer": "Please provide a question.", "sources": []}

    q_vec = embed_texts([question])[0]
    q = get_qdrant()
    results = q.search(q_vec, top_k=5, filters=filters or {})

    # Filter by score — require at least 0.3 similarity to avoid hallucination
    MIN_SCORE = 0.3
    relevant = [r for r in results if r.score >= MIN_SCORE]

    # Additional semantic filter: ensure doc metadata/text matches query intent
    if relevant and not _is_relevant(question, relevant):
        return {"answer": "No relevant data found for your query. Try asking about the uploaded companies or topics.", "sources": []}

    context = [r.payload.get("text", "") for r in relevant]
    sources = []
    for r in relevant:
        p = r.payload
        sources.append({
            "filename": p.get("filename"),
            "company": p.get("company"),
            "round_type": p.get("round_type"),
            "topic": p.get("topic"),
            "year": p.get("year"),
            "page": p.get("page"),
            "text": p.get("text")
        })

    if not relevant:
        return {"answer": "No relevant data found for your query. Try asking about the uploaded companies or topics.", "sources": []}

    joined = "\n\n".join(context[:5])
    prompt = f"Question: {question}\n\nContext:\n{joined}\n\nProvide the most repeated and high-priority questions/topics."
    answer = groq_chat(prompt)
    return {"answer": answer, "sources": sources}


def answer_question_stream(question: str, filters: dict | None = None):
    if not question:
        yield {"type": "error", "message": "Please provide a question."}
        return

    q_vec = embed_texts([question])[0]
    q = get_qdrant()
    results = q.search(q_vec, top_k=5, filters=filters or {})

    # Filter by score
    MIN_SCORE = 0.3
    relevant = [r for r in results if r.score >= MIN_SCORE]

    # Additional semantic filter
    if relevant and not _is_relevant(question, relevant):
        yield {"type": "answer", "content": "No relevant data found for your query. Try asking about the uploaded companies or topics."}
        yield {"type": "sources", "items": []}
        return

    context = [r.payload.get("text", "") for r in relevant]
    sources = []
    for r in relevant:
        p = r.payload
        sources.append({
            "filename": p.get("filename"),
            "company": p.get("company"),
            "round_type": p.get("round_type"),
            "topic": p.get("topic"),
            "year": p.get("year"),
            "page": p.get("page"),
        })

    if not relevant:
        yield {"type": "answer", "content": "No relevant data found for your query. Try asking about the uploaded companies or topics."}
        yield {"type": "sources", "items": []}
        return

    joined = "\n\n".join(context[:5])
    prompt = f"Question: {question}\n\nContext:\n{joined}\n\nProvide the most repeated and high-priority questions/topics."

    yield {"type": "sources", "items": sources}
    for delta in groq_chat_stream(prompt):
        yield {"type": "answer", "delta": delta}
