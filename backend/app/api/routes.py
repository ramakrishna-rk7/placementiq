from fastapi import APIRouter, UploadFile, File, Form, Body, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Document
from app.services.auth import signup, login, create_access_token
from app.services.rag import answer_question, index_document
from app.services.analytics import repeated_topics, semantic_topics
from app.services.deps import get_current_user
from jose import jwt
from app.config import JWT_SECRET_KEY, JWT_ALGORITHM, GROQ_API_KEY, GROQ_MODEL

router = APIRouter()


@router.get('/debug/token')
async def debug_token(authorization: str | None = Header(default=None)):
    return {
        "raw_header": repr(authorization),
        "starts_with_bearer": bool(authorization and authorization.startswith('Bearer ')),
        "header_length": len(authorization) if authorization else 0,
    }


@router.get('/debug/config')
async def debug_config():
    return {
        "groq_key_configured": bool(GROQ_API_KEY),
        "groq_key_length": len(GROQ_API_KEY),
        "groq_key_preview": GROQ_API_KEY[:8] + "..." if GROQ_API_KEY else "EMPTY",
        "groq_model": GROQ_MODEL,
    }


@router.get('/debug/test-token')
async def debug_test_token():
    tok = create_access_token({"sub": "1", "role": "admin"})
    try:
        payload = jwt.decode(tok, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return {"token": tok, "decoded": payload}
    except Exception as e:
        return {"token": tok, "error": str(e)}


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/auth/signup')
async def auth_signup(payload: dict = Body(...)):
    try:
        email = payload.get('email')
        password = payload.get('password')
        role = payload.get('role', 'student')
        db: Session = next(get_db())
        return signup(db, email, password, role)
    except Exception as e:
        import traceback
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": traceback.format_exc()})


@router.post('/auth/login')
async def auth_login(payload: dict = Body(...)):
    email = payload.get('email')
    password = payload.get('password')
    db: Session = next(get_db())
    return login(db, email, password)


@router.post('/documents/upload')
async def upload_document(
    file: UploadFile = File(...),
    company: str = Form(...),
    round_type: str = Form(...),
    topic: str = Form(''),
    year: int = Form(2025),
    authorization: str | None = Header(default=None)
):
    try:
        db: Session = next(get_db())
        # Auth bypassed for MVP — add role check here before going to prod
        data = await file.read()
        metadata = {"company": company, "round_type": round_type, "topic": topic, "year": year, "filename": file.filename}
        res = index_document(file.filename, data, metadata)
        if 'error' in res:
            return JSONResponse(status_code=400, content=res)
        doc = Document(
            filename=file.filename, company=company, round_type=round_type,
            topic=topic, year=year, uploaded_by=None
        )
        db.add(doc)
        db.commit()
        return {**res, "document_id": doc.id}
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        return JSONResponse(status_code=500, content={"error": str(e), "traceback": tb[-2000:]})


@router.post('/query')
async def query(payload: dict = Body(...)):
    question = payload.get('question', '')
    filters = payload.get('filters')
    return answer_question(question, filters)


@router.get('/analytics/repeated-topics')
async def analytics(authorization: str | None = Header(default=None)):
    db: Session = next(get_db())
    if authorization:
        get_current_user(db, authorization)
    return repeated_topics(db)


@router.get('/analytics/semantic-topics')
async def semantic_analytics(authorization: str | None = Header(default=None)):
    db: Session = next(get_db())
    if authorization:
        get_current_user(db, authorization)
    return semantic_topics(db)
