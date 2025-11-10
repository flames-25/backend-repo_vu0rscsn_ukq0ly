from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict
import os

from database import get_db, create_document, get_documents
from schemas import Lead

app = FastAPI(title="Pre-Purchase Inspection API")

# CORS settings - allow frontend
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*" if FRONTEND_URL == "*" else FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root() -> Dict[str, Any]:
    return {"message": "Pre-Purchase Inspection API is running"}

@app.get("/test")
async def test_connection() -> Dict[str, Any]:
    # Touch DB and list collections
    db = await get_db()
    cols = await db.list_collection_names()
    return {
        "backend": "ok",
        "database": "mongo",
        "database_url": os.getenv("DATABASE_URL", "mongodb://localhost:27017"),
        "database_name": os.getenv("DATABASE_NAME", "appdb"),
        "connection_status": "ok",
        "collections": cols,
    }

@app.post("/leads")
async def create_lead(lead: Lead) -> Dict[str, Any]:
    try:
        saved = await create_document("lead", lead.model_dump())
        return {"status": "ok", "lead": saved}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/leads")
async def list_leads() -> Dict[str, Any]:
    docs = await get_documents("lead", {}, 100)
    return {"items": docs}
