# PlacementIQ — AI Placement Intelligence System (RAG-Based)

## Project Overview

A RAG-based AI platform that analyzes company-wise placement data and helps students discover the most repeated and most likely interview, coding, and aptitude questions.

---

## Tech Stack

| Layer          | Technology                                                          |
| -------------- | ------------------------------------------------------------------- |
| Frontend       | Next.js 14 (React 18)                                               |
| Backend        | FastAPI (Python 3.12)                                               |
| AI Model       | Groq Llama 3.3-70B Versatile (via REST API)                         |
| Embeddings     | sentence-transformers (all-MiniLM-L6-v2, 384-dim)                   |
| Vector DB      | Qdrant (in-memory for local dev, server for production)             |
| Database       | SQLite via SQLAlchemy (swappable to PostgreSQL)                     |
| Auth           | JWT (python-jose) + PBKDF2 password hashing                         |

---

## Project Structure

```
placementiq/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py          # All API endpoints
│   │   ├── services/
│   │   │   ├── auth.py            # JWT auth + password hashing
│   │   │   ├── rag.py             # RAG pipeline (retrieve + LLM)
│   │   │   ├── analytics.py       # Topic frequency analytics
│   │   │   ├── deps.py            # Auth dependency injection
│   │   │   ├── doc_processing.py  # PDF/DOCX/TXT text extraction
│   │   │   ├── embeddings.py      # sentence-transformers wrapper
│   │   │   └── qdrant_client.py   # Qdrant vector DB wrapper
│   │   ├── config.py              # Environment config (.env)
│   │   ├── db.py                  # SQLAlchemy engine + session
│   │   ├── models.py              # User + Document ORM models
│   │   └── main.py                # FastAPI app entry point
│   ├── .env                       # Environment variables
│   └── requirements.txt           # Python dependencies
├── frontend/
│   ├── app/
│   │   ├── page.js                # Home / Landing page
│   │   ├── layout.js              # Root layout + nav
│   │   ├── globals.css            # Dark theme styles
│   │   ├── dashboard/page.js      # Student dashboard
│   │   ├── query/page.js          # AI query interface
│   │   └── admin/
│   │       ├── upload/page.js     # Document upload
│   │       └── analytics/page.js  # Topic analytics
│   ├── services/api.js            # API client (axios)
│   ├── package.json               # Node dependencies
│   └── next.config.mjs            # Next.js config
└── docs/
    └── PROJECT_REPORT.md          # This file
```

---

## API Endpoints

### Auth
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/signup` | No | Create account (email, password, role) |
| POST | `/auth/login` | No | Login, returns JWT token |

### Documents
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/documents/upload` | Bearer | Upload PDF/DOCX/TXT with metadata |

### Query
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/query` | No | Ask placement questions with optional filters |

### Analytics
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/analytics/repeated-topics` | Bearer | Get topic frequency counts |

### Debug
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/debug/config` | No | Check Groq API key status |
| GET | `/debug/token` | No | Debug auth header parsing |
| GET | `/debug/test-token` | No | Test JWT token generation |

---

## RAG Pipeline Flow

```
1. User uploads PDF/DOCX/TXT
2. Text extraction (pdfplumber / python-docx)
3. Text cleaning (normalize whitespace)
4. Chunking (800 words, 120 word overlap)
5. Embedding (all-MiniLM-L6-v2 → 384-dim vector)
6. Store in Qdrant (vector + metadata)
7. User asks a question
8. Question embedded into query vector
9. Qdrant searches top-5 similar chunks (with company/round filters)
10. Retrieved context sent to Groq Llama-3.3-70B
11. LLM generates answer with high-priority topics
12. Answer returned to user
```

---

## How to Run

### Prerequisites
- Python 3.12+
- Node.js 18+
- Groq API key (https://console.groq.com)

### Backend
```bash
cd placementiq/backend
# Create virtual environment
python -m venv .venv
# Activate (Windows)
source .venv/Scripts/activate
# Install dependencies
pip install -r requirements.txt
# Configure .env with your Groq key
echo "GROQ_API_KEY=gsk_your_key_here" >> .env
# Start server
python -m uvicorn app.main:app --host 0.0.0.0 --port 18081
```

### Frontend
```bash
cd placementiq/frontend
npm install
npm run dev
```

Open http://localhost:3000 in your browser.

---

## Build Steps (What Was Done)

### Phase 1: Project Scaffolding
1. Created directory structure (frontend, backend, docs, scripts)
2. Wrote project README and PRD documentation
3. Created Next.js frontend with 6 pages (home, dashboard, query, admin upload, analytics)
4. Created FastAPI backend with modular architecture

### Phase 2: Backend Core
5. Implemented SQLAlchemy models (User, Document) with SQLite
6. Built JWT authentication with PBKDF2 password hashing
7. Created document processing pipeline (PDF/DOCX/TXT extraction)
8. Built chunking engine (800-word chunks, 120-word overlap)
9. Implemented sentence-transformers embedding service
10. Created Qdrant vector DB wrapper with auto-fallback to in-memory

### Phase 3: RAG Pipeline
11. Built retrieval service with company/round/topic filters
12. Integrated Groq Llama-3.3-70B API for LLM answer generation
13. Built analytics service (topic frequency counting via SQL)
14. Added debug endpoints for configuration verification

### Phase 4: Frontend Integration
15. Connected frontend API service to backend endpoints
16. Built admin upload page with form metadata
17. Built AI query page with text input and answer display
18. Built analytics display page
19. Updated API base URL to match running backend port

### Phase 5: Testing & Verification
20. Tested all 5 core endpoints (signup, login, upload, query, analytics)
21. Fixed module/directory conflicts (removed `__init__.py` from app/ subdirectories)
22. Replaced passlib bcrypt with built-in PBKDF2 (Python 3.12 compatibility)
23. Pre-downloaded sentence-transformer model to avoid first-query timeout
24. Verified full RAG pipeline: upload → embed → store → retrieve → LLM answer
25. Cleaned up test files and cached bytecode

---

## Test Results (Final)

| Test | Status | Details |
|------|--------|---------|
| Signup | ✅ | Creates user, returns user object |
| Login | ✅ | Returns 139-char JWT token |
| Upload (TXT) | ✅ | Extracts text, chunks, embeds, indexes to Qdrant |
| Query (Infosys coding) | ✅ | LLM returns arrays, linked lists, strings as high-priority topics |
| Query (TCS DBMS) | ✅ | LLM returns SQL Joins, Normalization, ACID as high-priority |
| Analytics | ✅ | Counts topics: arrays=1, dbms=1 |
| Auth protection | ✅ | Returns 401 without valid token |

---

## Configuration

All configuration is in `backend/.env`:

```
DATABASE_URL=sqlite:///./placementiq.db
JWT_SECRET_KEY=change-me-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
QDRANT_URL=http://localhost:6333
```

---

## Future Enhancements

- PostgreSQL instead of SQLite for production
- Qdrant server instead of in-memory for persistent vectors
- Voice interview AI
- Mock interview simulation
- Resume analysis
- Placement prediction analytics
- Real-time chat
- Mobile app

---

## License

Internal project — PlacementIQ
