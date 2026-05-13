import os
from dotenv import load_dotenv

load_dotenv()

# Use SQLite for zero-dependency local dev
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./placementiq.db')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'change-me-secret-key')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_EXPIRE_MINUTES = int(os.getenv('JWT_EXPIRE_MINUTES', '60'))
GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
QDRANT_URL = os.getenv('QDRANT_URL', 'http://localhost:6333')
QDRANT_API_KEY = os.getenv('QDRANT_API_KEY', '')