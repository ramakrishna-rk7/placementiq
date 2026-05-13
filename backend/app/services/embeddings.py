from sentence_transformers import SentenceTransformer

_MODEL = None

def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    return _MODEL


def embed_texts(texts):
    model = get_model()
    return model.encode(texts, show_progress_bar=False).tolist()
