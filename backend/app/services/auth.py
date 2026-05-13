from datetime import datetime, timedelta
from hashlib import pbkdf2_hmac
from secrets import token_hex
from jose import jwt
from sqlalchemy.orm import Session
from app.config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MINUTES
from app.models import User

def _hash(password: str) -> str:
    salt = token_hex(16)
    h = pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    return f'{salt}${h}'

def _verify(password: str, stored: str) -> bool:
    salt, h = stored.split('$', 1)
    return pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex() == h

def create_access_token(data: dict, expires_minutes: int = JWT_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def signup(db: Session, email: str, password: str, role: str):
    if db.query(User).filter(User.email == email).first():
        return {"error": "User already exists"}
    user = User(email=email, password_hash=_hash(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Signed up", "user": {"id": user.id, "email": user.email, "role": user.role}}

def login(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not _verify(password, user.password_hash):
        return {"error": "Invalid credentials"}
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"message": "Logged in", "token": token, "user": {"id": user.id, "email": user.email, "role": user.role}}
