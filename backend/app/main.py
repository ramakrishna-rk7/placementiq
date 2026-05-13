from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.api.stream import router as stream_router
from app.db import Base, engine, _migrate_documents_table

app = FastAPI(title='PlacementIQ API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

_migrate_documents_table()
Base.metadata.create_all(bind=engine)
app.include_router(router)
app.include_router(stream_router)
