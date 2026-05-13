import io
import pdfplumber
from docx import Document


def extract_text_from_pdf(data: bytes):
    # returns (text, page_map)
    page_map = []
    text = []
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        for idx, page in enumerate(pdf.pages, start=1):
            t = page.extract_text() or ''
            if t:
                page_map.append({"page": idx, "text": t})
                text.append(t)
    return '\n'.join(text), page_map


def extract_text_from_docx(data: bytes):
    doc = Document(io.BytesIO(data))
    text = '\n'.join([p.text for p in doc.paragraphs if p.text])
    # DOCX doesn't have pages reliably; use page=1
    return text, [{"page": 1, "text": text}]


def extract_text(filename: str, data: bytes):
    lower = filename.lower()
    if lower.endswith('.pdf'):
        return extract_text_from_pdf(data)
    if lower.endswith('.docx'):
        return extract_text_from_docx(data)
    if lower.endswith('.txt'):
        text = data.decode('utf-8', errors='ignore')
        return text, [{"page": 1, "text": text}]
    return '', []


def clean_text(text: str) -> str:
    return ' '.join(text.split())


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120):
    words = text.split(' ')
    chunks = []
    i = 0
    while i < len(words):
        chunk = words[i:i+chunk_size]
        if chunk:
            chunks.append(' '.join(chunk))
        i += max(chunk_size - overlap, 1)
    return chunks


def chunk_text_with_pages(page_map, chunk_size: int = 800, overlap: int = 120):
    # page_map: list of {page, text}
    # chunk each page independently to preserve page numbers
    chunks = []
    for item in page_map:
        page = item['page']
        page_text = clean_text(item['text'])
        if not page_text:
            continue
        page_chunks = chunk_text(page_text, chunk_size=chunk_size, overlap=overlap)
        for c in page_chunks:
            chunks.append({"text": c, "page": page})
    return chunks
