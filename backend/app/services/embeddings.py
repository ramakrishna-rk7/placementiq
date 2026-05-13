from fastembed import TextEmbedding

_MODEL = None

def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = TextEmbedding(model_name="BAAI/bge-small-en")
    return _MODEL


def embed_texts(texts):
    model = get_model()
    return [list(e) for e in model.embed(texts)]
