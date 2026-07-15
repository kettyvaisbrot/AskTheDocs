from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.database import init_db
from app.documents import list_documents
from app.ingest import ingest_document
from app.schemas import AskRequest, DocumentDetail, DocumentOut, IngestRequest
from app.search import keyword_search


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Ask the Docs", lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = exc.errors()
    message = errors[0]["msg"] if errors else "invalid request"
    return JSONResponse(status_code=422, content={"error": message})


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Ask the Docs"}


@app.post("/ingest", response_model=DocumentOut, status_code=201)
def ingest(payload: IngestRequest, response: Response):
    try:
        document, created = ingest_document(payload.url, payload.text)
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    response.status_code = 201 if created else 200
    return document


@app.get("/documents", response_model=list[DocumentDetail])
def get_documents():
    return list_documents()


@app.post("/ask")
def ask(payload: AskRequest):
    snippet = keyword_search(payload.question)
    if snippet is None:
        return {"answer": "לא נמצאה התאמה במסמכים השמורים"}
    return {"answer": snippet}
