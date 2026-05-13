from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from app.config import QDRANT_URL, QDRANT_API_KEY

COLLECTION = 'placementiq'

class QdrantWrapper:
    def __init__(self):
        if not QDRANT_URL:
            raise RuntimeError('QDRANT_URL is not configured. Set it in .env')
        # Require a running Qdrant server (persistent vectors)
        args = {"url": QDRANT_URL}
        if QDRANT_API_KEY:
            args["api_key"] = QDRANT_API_KEY
        self.client = QdrantClient(**args)
        # Fail fast if server is unreachable
        self.client.get_collections()
        self._ensure_collection()

    def _ensure_collection(self, vector_size: int = 384):
        exists = self.client.get_collections().collections
        if not any(c.name == COLLECTION for c in exists):
            self.client.create_collection(
                collection_name=COLLECTION,
                vectors_config=rest.VectorParams(size=vector_size, distance=rest.Distance.COSINE)
            )

    def upsert(self, vectors, payloads):
        points = []
        for vec, payload in zip(vectors, payloads):
            points.append(rest.PointStruct(id=payload['id'], vector=vec, payload=payload))
        self.client.upsert(collection_name=COLLECTION, points=points)

    def search(self, vector, top_k=5, filters=None):
        flt = None
        if filters:
            conditions = []
            for k, v in filters.items():
                conditions.append(rest.FieldCondition(key=k, match=rest.MatchValue(value=str(v))))
            flt = rest.Filter(must=conditions)
        return self.client.search(collection_name=COLLECTION, query_vector=vector, limit=top_k, query_filter=flt)

    def scroll_all(self, limit=1000):
        # Return all points with payload and vectors
        points = []
        offset = None
        while True:
            batch, offset = self.client.scroll(
                collection_name=COLLECTION,
                limit=limit,
                with_payload=True,
                with_vectors=True,
                offset=offset
            )
            points.extend(batch)
            if offset is None or len(batch) == 0:
                break
        return points


_qdrant = None
def get_qdrant():
    global _qdrant
    if _qdrant is None:
        _qdrant = QdrantWrapper()
    return _qdrant
