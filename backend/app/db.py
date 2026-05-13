from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import DATABASE_URL

# SQLite special handling
if DATABASE_URL.startswith('sqlite'):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_pre_ping=True,
    )
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass


def _migrate_documents_table():
    """Fix uploaded_by NOT NULL constraint for existing SQLite dbs."""
    if not DATABASE_URL.startswith('sqlite'):
        return
    with engine.connect() as conn:
        try:
            # Check if the column is NOT NULL
            result = conn.execute(text("PRAGMA table_info(documents)"))
            cols = {row[1]: row[5] for row in result}  # name -> notnull
            if cols.get('uploaded_by', 1) != 0:
                # Column is NOT NULL (notnull=1). Rename, recreate, copy data.
                conn.execute(text("ALTER TABLE documents RENAME TO documents_old"))
                conn.execute(text("""CREATE TABLE documents (
                    id INTEGER PRIMARY KEY,
                    filename VARCHAR NOT NULL,
                    company VARCHAR NOT NULL,
                    round_type VARCHAR NOT NULL,
                    topic VARCHAR NOT NULL,
                    year INTEGER NOT NULL,
                    uploaded_by INTEGER
                )"""))
                conn.execute(text("INSERT INTO documents SELECT * FROM documents_old"))
                conn.execute(text("DROP TABLE documents_old"))
                conn.commit()
        except Exception:
            # Table might not exist yet — let create_all handle it
            pass