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


def answer_question(question: str, filters: dict | None = None):
    if not question:
        return {"answer": "Please provide a question.", "sources": []}

    q_vec = embed_texts([question])[0]
    q = get_qdrant()
    results = q.search(q_vec, top_k=5, filters=filters or {})

    context = [r.payload.get("text", "") for r in results]
    sources = []
    for r in results:
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

    if not context:
        return {"answer": "No relevant data found. Try uploading documents first.", "sources": []}

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

    context = [r.payload.get("text", "") for r in results]
    sources = []
    for r in results:
        p = r.payload
        sources.append({
            "filename": p.get("filename"),
            "company": p.get("company"),
            "round_type": p.get("round_type"),
            "topic": p.get("topic"),
            "year": p.get("year"),
            "page": p.get("page"),
        })

    if not context:
        yield {"type": "answer", "content": "No relevant data found. Try uploading documents first."}
        yield {"type": "sources", "items": []}
        return

    joined = "\n\n".join(context[:5])
    prompt = f"Question: {question}\n\nContext:\n{joined}\n\nProvide the most repeated and high-priority questions/topics."

    yield {"type": "sources", "items": sources}
    for delta in groq_chat_stream(prompt):
        yield {"type": "answer", "delta": delta}
