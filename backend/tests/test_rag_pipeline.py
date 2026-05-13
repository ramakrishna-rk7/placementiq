import io
import pytest
from app.services.doc_processing import extract_text, chunk_text, chunk_text_with_pages
from app.services.embeddings import embed_texts


def test_extract_text_txt():
    text, pages = extract_text("sample.txt", b"Hello world")
    assert "Hello" in text
    assert pages and pages[0]["page"] == 1


def test_chunk_text_basic():
    text = "word " * 1000
    chunks = chunk_text(text, chunk_size=100, overlap=10)
    assert len(chunks) > 1


def test_chunk_text_with_pages():
    page_map = [
        {"page": 1, "text": "alpha beta gamma"},
        {"page": 2, "text": "delta epsilon zeta"}
    ]
    chunks = chunk_text_with_pages(page_map, chunk_size=2, overlap=1)
    assert all("page" in c for c in chunks)
    assert {c["page"] for c in chunks} == {1, 2}


def test_embeddings_dimension():
    vecs = embed_texts(["hello world", "test sentence"])
    assert len(vecs) == 2
    assert len(vecs[0]) == len(vecs[1])


@pytest.mark.parametrize("question", [
    "Most repeated Infosys coding questions",
    "Important DBMS questions for TCS"
])
def test_dummy_queries(question):
    # Smoke test for embedding pipeline
    vec = embed_texts([question])[0]
    assert len(vec) > 0
