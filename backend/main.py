from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.pipeline import ResearchPipeline
from database.faiss_store import FaissKnowledgeBase
from database.storage import LocalStorage, ReportRecord, new_report_id, utc_now_iso

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Autonomous Energy Researcher Agent", version="1.0.0")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
pipeline = ResearchPipeline()
kb = FaissKnowledgeBase()
storage = LocalStorage()

# Startup event - show backend is running
@app.on_event("startup")
async def startup_event():
    logger.info("✅ Backend initialized successfully!")
    logger.info("📡 Connected components: ResearchPipeline, Knowledge Base, LocalStorage")
    logger.info("🚀 Backend is running and ready to receive requests from frontend")


class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)


class SimilarityRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)
    k: int = Field(5, ge=1, le=10)


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"ok": True}


@app.post("/research")
def research(req: ResearchRequest) -> Dict[str, Any]:
    logger.info(f"🔍 Received research query: {req.query[:50]}...")
    logger.info("🚀 Starting pipeline execution...")
    try:
        result = pipeline.run(req.query)
        logger.info(f"✅ Research completed successfully for query: {req.query[:50]}...")

        report_id = new_report_id()
        report = result["report"]

        record = ReportRecord(
            id=report_id,
            query=req.query,
            title=report["title"],
            introduction=report["introduction"],
            key_findings=report["key_findings"],
            conclusion=report["conclusion"],
            sources=result["sources"],
            created_at=utc_now_iso().replace(":", "").replace("-", ""),
        )

        storage.save_report(record)

        report_text = "\n".join(
            [
                record.title,
                "",
                record.introduction,
                "",
                "Key Findings:",
                *[f"- {k}" for k in record.key_findings],
                "",
                record.conclusion,
            ]
        )
        kb.add_report(report_id=record.id, query=record.query, report_text=report_text)
        logger.info(f"💾 Report saved with ID: {report_id}")
        return {"report_id": report_id, **result}
    except Exception as e:
        logger.error(f"❌ Error during research: {str(e)}")
        raise


@app.get("/reports")
def list_reports(limit: int = 20) -> Dict[str, Any]:
    items = storage.list_reports(limit=limit)
    return {"reports": [r.__dict__ for r in items]}


@app.post("/similarity_search")
def similarity_search(req: SimilarityRequest) -> Dict[str, Any]:
    logger.info(f"🔎 Similarity search for: {req.query[:50]}...")
    try:
        docs = kb.similarity_search(req.query, k=req.k)
        out: List[Dict[str, Any]] = []
        for d in docs:
            out.append(
                {
                    "content_preview": (d.page_content[:400] + "...") if len(d.page_content) > 400 else d.page_content,
                    "metadata": d.metadata,
                }
            )
        logger.info(f"✅ Found {len(out)} similar documents")
        return {"results": out}
    except Exception as e:
        logger.error(f"❌ Error during similarity search: {str(e)}")
        raise

