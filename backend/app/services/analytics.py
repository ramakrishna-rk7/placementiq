from sqlalchemy.orm import Session
from app.models import Document
from app.services.qdrant_client import get_qdrant
from app.services.embeddings import embed_texts
import math


def repeated_topics(db: Session):
    # legacy: DB-based counts
    rows = db.query(Document.topic, Document.year).all()
    counts = {}
    for topic, _ in rows:
        if not topic:
            continue
        counts[topic] = counts.get(topic, 0) + 1
    items = [{"topic": k, "count": v} for k, v in sorted(counts.items(), key=lambda x: -x[1])]
    return {"items": items}


def _cosine(a, b):
    num = sum(x*y for x, y in zip(a, b))
    da = math.sqrt(sum(x*x for x in a))
    db = math.sqrt(sum(x*x for x in b))
    if da == 0 or db == 0:
        return 0.0
    return num / (da * db)


def semantic_topics(db: Session, k: int = 5, max_points: int = 500):
    # Pull vectors from Qdrant and cluster using simple k-means
    q = get_qdrant()
    points = q.scroll_all(limit=max_points)
    if not points:
        return {"clusters": []}

    vectors = [p.vector for p in points]
    texts = [p.payload.get("text", "") for p in points]

    # Initialize centroids with first k vectors
    k = min(k, len(vectors))
    centroids = vectors[:k]
    assignments = [0] * len(vectors)

    for _ in range(5):
        # assign
        for i, v in enumerate(vectors):
            best = 0
            best_sim = -1
            for c_idx, c in enumerate(centroids):
                sim = _cosine(v, c)
                if sim > best_sim:
                    best_sim = sim
                    best = c_idx
            assignments[i] = best
        # update centroids
        new_centroids = []
        for ci in range(k):
            group = [vectors[i] for i, a in enumerate(assignments) if a == ci]
            if not group:
                new_centroids.append(centroids[ci])
                continue
            dim = len(group[0])
            avg = [0.0] * dim
            for v in group:
                for d in range(dim):
                    avg[d] += v[d]
            avg = [x/len(group) for x in avg]
            new_centroids.append(avg)
        centroids = new_centroids

    # Label clusters using top terms from texts (simple frequency)
    clusters = []
    for ci in range(k):
        group_texts = [texts[i] for i, a in enumerate(assignments) if a == ci]
        freq = {}
        for t in group_texts:
            for w in t.lower().split():
                if len(w) < 4:
                    continue
                freq[w] = freq.get(w, 0) + 1
        top_terms = sorted(freq.items(), key=lambda x: -x[1])[:5]
        label = ", ".join([w for w, _ in top_terms]) if top_terms else f"Cluster {ci+1}"
        clusters.append({
            "label": label,
            "count": len(group_texts),
            "top_terms": [w for w, _ in top_terms]
        })

    return {"clusters": clusters}
