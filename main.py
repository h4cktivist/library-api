from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.endpoints import auth, books, reader, borrowing
from core.config import settings


app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(books.router, prefix='/books', tags=['books'])
app.include_router(reader.router, prefix='/readers', tags=['readers'])
app.include_router(borrowing.router, prefix='/borrowings', tags=['borrowings'])
