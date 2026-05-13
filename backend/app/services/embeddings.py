import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

_VECTORIZER = None

def get_vectorizer():
    global _VECTORIZER
    if _VECTORIZER is None:
        _VECTORIZER = TfidfVectorizer(
            max_features=384,
            stop_words='english',
            sublinear_tf=True,
        )
    return _VECTORIZER


def embed_texts(texts):
    vec = get_vectorizer()
    # Fit on first call, transform thereafter
    if not hasattr(vec, 'vocabulary_'):
        matrix = vec.fit_transform(texts)
    else:
        matrix = vec.transform(texts)
    # Convert to dense list-of-lists
    return matrix.toarray().tolist()
