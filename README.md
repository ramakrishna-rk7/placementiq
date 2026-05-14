# PlacementIQ

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Next.js](https://img.shields.io/badge/Next.js-14.2.5-black?logo=nextdotjs&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-Cloud-ef4444?logo=qdrant&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLM-7c3aed)
![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.4-38bdf8?logo=tailwindcss&logoColor=white)
![License](https://img.shields.io/badge/license-portfolio-lightgrey)
![Repo Size](https://img.shields.io/github/repo-size/ramakrishna-rk7/placementiq)
![Last Commit](https://img.shields.io/github/last-commit/ramakrishna-rk7/placementiq)
![Top Language](https://img.shields.io/github/languages/top/ramakrishna-rk7/placementiq)

PlacementIQ is a full-stack AI platform for placement preparation. It helps students, job seekers, and campus placement teams upload interview documents, search them with semantic retrieval, and generate high-signal answers with page-level citations.

It is built as a practical, deployable product rather than a toy demo. The project combines document ingestion, vector search, streaming generation, semantic analytics, and authentication into one polished experience.

## Live Demo

- Frontend: https://placementiq-peach.vercel.app

## Repository

- GitHub: https://github.com/ramakrishna-rk7/placementiq

## What PlacementIQ Does

PlacementIQ turns placement materials into a searchable, explainable knowledge base.

Core capabilities:
- Upload placement papers, interview notes, HR guides, and preparation documents
- Extract text from PDF, DOCX, and TXT files
- Chunk documents into retrieval-friendly segments
- Store embeddings and metadata in Qdrant Cloud for persistent semantic search
- Ask natural-language questions and receive streamed answers
- Show citations with filename and page number when available
- Analyze document collections through semantic clustering
- Support authentication with JWT-based login and signup endpoints

## Why Recruiters and Interviewers Should Care

PlacementIQ demonstrates the kind of engineering that matters in real products:

- Full-stack architecture: separate frontend, backend, vector database, and LLM provider
- Retrieval-augmented generation: grounded answers from document context, not generic chat output
- Streaming UX: answers arrive incrementally via Server-Sent Events
- Explainability: responses include source metadata and citations
- Production constraints awareness: lightweight embeddings instead of expensive model stacks
- Cloud deployment experience: Vercel, Render, Qdrant Cloud, and Groq integration
- Clean service boundaries: document processing, embeddings, retrieval, analytics, and auth are separated

## Key Features

### 1. Document Upload and Indexing
Users can upload documents and attach metadata such as:
- Company name
- Round type
- Topic
- Year

The backend then:
- extracts text
- cleans and chunks it
- generates embeddings
- stores chunks in Qdrant with metadata

### 2. Streaming AI Query Experience
The query page provides a chat-like interface that streams responses as they are generated.

This makes the experience feel responsive and modern, while keeping the backend simple through a FastAPI SSE endpoint.

### 3. Citation-Aware Retrieval
Each answer can include source metadata such as:
- filename
- company
- round type
- topic
- year
- page number

This makes the system easier to trust during interview prep and easier to debug during development.

### 4. Semantic Analytics
PlacementIQ includes analytics that go beyond raw counts:
- repeated-topic summaries
- semantic clustering over stored embeddings
- cluster labels based on dominant terms
- visual charts for quick insight

### 5. Auth and Access Control
The backend includes basic signup/login flows with:
- password hashing
- JWT access tokens
- role support
- protected analytics endpoints

## Tools and Technologies

### Frontend
- Next.js 14
- React 18
- Tailwind CSS
- Framer Motion
- Recharts
- Lucide React
- Axios

### Backend
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- python-jose
- python-multipart
- pdfplumber
- python-docx
- scikit-learn
- Qdrant client

### Infrastructure and Services
- Vercel for frontend hosting
- Render for backend hosting
- Qdrant Cloud for vector persistence
- Groq for LLM inference

## Architecture Overview

```text
User
  -> Next.js frontend
  -> FastAPI backend
  -> document extraction + cleaning
  -> embedding generation
  -> Qdrant vector search
  -> Groq response generation
  -> streamed answer + citations
```

Data flow:
1. User uploads placement material
2. Backend extracts and chunks text
3. TF-IDF embeddings are generated
4. Chunks are stored in Qdrant with metadata
5. User asks a question
6. Backend retrieves relevant chunks from Qdrant
7. Groq generates a concise answer from the retrieved context
8. Frontend renders the answer live with citations

## Project Structure

```text
placementiq/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── main.py
│   │   └── models.py
│   ├── requirements.txt
│   └── render.yaml
├── frontend/
│   ├── app/
│   ├── services/
│   └── package.json
├── runtime.txt
└── README.md
```

## Frontend Pages

- `/` — landing page
- `/query` — streaming AI search interface
- `/dashboard` — student dashboard overview
- `/admin/upload` — document upload and tagging
- `/admin/analytics` — semantic analytics charts

## Backend API Highlights

- `POST /auth/signup` — create user account
- `POST /auth/login` — generate JWT token
- `POST /documents/upload` — upload and index placement docs
- `POST /query` — answer a question using retrieved context
- `POST /query/stream` — streaming version of the query endpoint
- `GET /analytics/repeated-topics` — topic frequency summary
- `GET /analytics/semantic-topics` — clustering-based analytics

## Local Development

### Prerequisites
- Python 3.12+
- Node.js 18+
- Qdrant Cloud account or local Qdrant endpoint
- Groq API key

### Backend Setup

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash
pip install -r requirements.txt
```

Create a `.env` file in `backend/`:

```env
DATABASE_URL=sqlite:///./placementiq.db
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
GROQ_API_KEY=your-groq-key
GROQ_MODEL=llama-3.3-70b-versatile
QDRANT_URL=https://your-qdrant-cluster.cloud.qdrant.io:6333
QDRANT_API_KEY=your-qdrant-api-key
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
```

Create a `.env.local` file in `frontend/`:

```env
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

Run the frontend:

```bash
npm run dev
```

## Deployment Notes

This project is deployed as a monorepo:
- Render serves the FastAPI backend from `backend/`
- Vercel serves the Next.js frontend from `frontend/`

Important deployment details:
- Set the backend Python version to 3.12 on Render
- Use a persistent Qdrant Cloud cluster
- Set `NEXT_PUBLIC_API_BASE` on Vercel to the deployed backend URL
- Redeploy Vercel after changing environment variables

## Notes on Embeddings

PlacementIQ uses TF-IDF embeddings instead of heavyweight transformer models.

Why:
- lower memory usage
- faster startup
- fewer deployment failures on free tiers
- no PyTorch or CUDA dependency

This keeps the app stable and easier to run in constrained environments.

## Security and Reliability Considerations

The project already reflects several real-world engineering concerns:
- password hashing for authentication
- JWT-based auth flow
- production CORS handling
- persistent vector storage
- fixed embedding dimensions for Qdrant compatibility
- page-aware citations for traceability
- streaming transport for better UX

## Recruiter-Facing Summary

PlacementIQ demonstrates:
- full-stack product thinking
- API design
- vector search and retrieval-augmented generation
- document processing pipelines
- streaming frontend/backend integration
- cloud deployment across multiple services
- practical tradeoff decisions under resource constraints

If you are reviewing this project for interviews, the strongest talking points are:
- persistent semantic retrieval over placement documents
- streamed answers with citations
- deployable architecture using real cloud services
- analytics built from embeddings rather than simple keyword counts

## Future Improvements

Potential next steps:
- stronger role-based authorization
- richer source highlighting inside documents
- Postgres persistence for user and metadata storage
- evaluation suite for retrieval quality
- better document preview and citation UI
- admin moderation for document quality

## License

This project is provided as part of the PlacementIQ portfolio.

---

Built to help students prepare smarter for placements, interviews, and technical screenings.
