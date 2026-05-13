import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

_VECTORIZER = None
VECTOR_SIZE = 384

def get_vectorizer():
    global _VECTORIZER
    if _VECTORIZER is None:
        _VECTORIZER = TfidfVectorizer(
            max_features=VECTOR_SIZE,
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
    # Convert to dense array
    dense = matrix.toarray()
    # Pad/truncate to fixed size
    if dense.shape[1] < VECTOR_SIZE:
        padded = np.zeros((dense.shape[0], VECTOR_SIZE))
        padded[:, :dense.shape[1]] = dense
        dense = padded
    elif dense.shape[1] > VECTOR_SIZE:
        dense = dense[:, :VECTOR_SIZE]
    return dense.tolist()
