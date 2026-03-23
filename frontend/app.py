from __future__ import annotations

import json
import os
from typing import Any, Dict, List

import requests
import streamlit as st


st.set_page_config(page_title="Autonomous Energy Researcher Agent", layout="wide")


def _get_backend_url() -> str:
    # Keep this Streamlit-safe: do NOT touch st.secrets here (it can trigger a
    # Streamlit command before page config in some environments).
    env = os.getenv("BACKEND_URL")
    if env:
        return env.strip().rstrip("/")
    return "http://127.0.0.1:8000"


BACKEND_URL = _get_backend_url()


def _post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        r = requests.post(f"{BACKEND_URL}{path}", json=payload, timeout=180)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to backend at {BACKEND_URL}. Is the backend running?")
        raise
    except requests.exceptions.Timeout:
        st.error("❌ Backend request timed out. The research took too long.")
        raise
    except Exception as e:
        st.error(f"❌ Backend error: {str(e)}")
        raise


def _get(path: str) -> Dict[str, Any]:
    try:
        r = requests.get(f"{BACKEND_URL}{path}", timeout=60)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        st.error(f"❌ Cannot connect to backend at {BACKEND_URL}. Is the backend running?")
        raise
    except Exception as e:
        st.error(f"❌ Error fetching from backend: {str(e)}")
        raise

st.title("Autonomous Energy Researcher Agent")

# Show backend connection status
try:
    health = _get("/health")
    st.success(f"✅ Connected to backend at {BACKEND_URL}")
except Exception as e:
    st.error(f"❌ Backend not available at {BACKEND_URL}")

query = st.text_input("Enter an energy research query", placeholder="e.g., What are the latest trends in grid-scale battery storage in 2025?")

col1, col2 = st.columns([1, 1])
with col1:
    run_btn = st.button("Generate Research", type="primary", disabled=not query.strip())
with col2:
    sim_btn = st.button("Search Stored Knowledge", disabled=not query.strip())

if run_btn:
    with st.spinner("Researching (searching + scraping + analyzing + summarizing)..."):
        try:
            data = _post("/research", {"query": query})

            report = data["report"]
            st.subheader(report["title"])
            st.markdown("### Introduction")
            st.write(report["introduction"])

            st.markdown("### Key Findings")
            for k in report["key_findings"]:
                st.write(f"- {k}")

            st.markdown("### Conclusion")
            st.write(report["conclusion"])

            st.markdown("### Sources")
            for s in data.get("sources", []):
                title = s.get("title") or s.get("url")
                st.write(f"- [{title}]({s.get('url')})")

            st.success(f"✅ Saved to knowledge base. Report ID: {data.get('report_id')}")
        except Exception as e:
            st.error(f"❌ Research failed. Check backend logs for details.")

if sim_btn:
    with st.spinner("Searching the knowledge base..."):
        try:
            results = _post("/similarity_search", {"query": query, "k": 5})
            st.markdown("### Similar Past Reports (by semantic similarity)")
            for r in results.get("results", []):
                meta = r.get("metadata") or {}
                st.write(f"**Report ID:** {meta.get('report_id')}  |  **Original query:** {meta.get('query')}")
                st.caption(r.get("content_preview") or "")
                st.divider()
        except Exception as e:
            st.error(f"❌ Search failed. Check backend logs for details.")

with st.expander("Previously stored reports"):
    try:
        reports = _get("/reports").get("reports", [])
        if not reports:
            st.caption("No stored reports yet.")
        else:
            for rec in reports:
                st.write(f"**{rec.get('title')}**")
                st.caption(f"Query: {rec.get('query')} | Created: {rec.get('created_at')} | ID: {rec.get('id')}")
                st.write(rec.get("introduction", ""))
                st.divider()
    except Exception as e:
        st.caption(f"Unable to load stored reports from backend: {e}")

