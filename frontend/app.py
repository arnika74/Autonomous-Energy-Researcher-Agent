from __future__ import annotations

import os
import re
from typing import Any, Dict, List

import requests
import streamlit as st

from styles import apply_theme


st.set_page_config(
    page_title="Autonomous Energy Researcher Agent",
    layout="wide",
    initial_sidebar_state="expanded"
)


def _get_backend_url() -> str:
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


def safe_rerun() -> None:
    if hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
    elif hasattr(st, "rerun"):
        st.rerun()
    else:
        st.warning("⚠️ Please manually refresh the page to apply routing changes.")


apply_theme()

backend_ok = False
try:
    _ = _get("/health")
    backend_ok = True
    if "backend_connected_toast" not in st.session_state:
        st.session_state.backend_connected_toast = True
        if hasattr(st, "toast"):
            st.toast("✅ Backend connected and ready!", icon="✅")
except Exception:
    st.error(f"❌ Backend not available at {BACKEND_URL}")
    st.warning("Please start the backend server (uvicorn backend.main:app --reload) and refresh this page.")


if "page" not in st.session_state:
    st.session_state.page = "home"
if "last_query" not in st.session_state:
    st.session_state.last_query = ""
if "current_report" not in st.session_state:
    st.session_state.current_report = None
if "history" not in st.session_state:
    st.session_state.history = []


def extract_key_findings(raw_text: str) -> List[str]:
    raw = raw_text.strip()
    if not raw:
        return []

    # Normalize bullet markers and numbering
    raw = raw.replace('•', '\n-').replace('*', '').replace('\r\n', '\n').replace('\r', '\n')
    raw = re.sub(r'\s*(\d+)\.\s*', '\n\1. ', raw)

    lines = []
    # split by numbered bullets if present
    if re.search(r'\n\s*\d+\.', raw):
        segments = re.split(r'\n\s*\d+\.', raw)
        for seg in segments:
            text = seg.strip()
            if text:
                lines.append(text)
    else:
        for line in raw.split('\n'):
            text = line.strip()
            if not text:
                continue
            if text.lower().startswith('here are') or text.lower().startswith('key findings'):
                continue
            if text.startswith('-'):
                text = text.lstrip('-•* ').strip()
            if text:
                lines.append(text)

    # dedupe and return
    seen = set()
    result = []
    for item in lines:
        normalized = item.strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


def load_history() -> None:
    try:
        reports = _get("/reports").get("reports", [])
        st.session_state.history = sorted(reports, key=lambda x: x.get("created_at", ""), reverse=True)
    except Exception:
        st.session_state.history = []


load_history()

st.markdown(
    """
    <div style='text-align: center; margin-bottom: 1rem;'>
    <div style='font-size: 3rem; font-weight: 800; letter-spacing: 1px; 
    color: #00d4ff; line-height: 1.2;'>
        ⚡ Autonomous Energy Researcher Agent ⚡
    </div>
    <p style='font-size: 1.35rem; color: #cbd5e1; margin: 8px 0 0 0;'>A powerful AI assistant for renewable energy research</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.page == "home":
    st.markdown(
        """
        <div class="highlight-section">
        <h3 style="margin-top: 0; color: #00d4ff;">🔬 Intelligent Energy Research at Your Fingertips</h3>
        <p style="color: #cbd5e1; font-size: 1.2rem; line-height: 1.8;">
        Ask complex energy questions and get comprehensive, research-backed answers in minutes.
        Our AI agents search, analyze, and synthesize information from multiple sources to deliver
        clear, actionable insights on renewable energy, grid technology, storage solutions, and more.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="highlight-section">
        <h2 style="margin-top: 0; color: #00d4ff; font-size: 2rem;">🎯 How It Works</h2>
        <p style="color: #cbd5e1; font-size: 1.05rem; line-height: 1.8; margin-bottom: 24px;">
        Our intelligent research pipeline combines web searching, knowledge extraction, and AI analysis
        to provide you with comprehensive, well-sourced energy insights:
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
   
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            """
            <div style="background: rgba(0, 212, 255, 0.1); border: 1px solid rgba(0, 212, 255, 0.3); border-radius: 12px; padding: 20px; text-align: center; animation: fadeInUp 0.6s ease-out;">
            <h3 style="color: #00d4ff; margin-top: 0;">🔍</h3>
            <h4 style="color: #0099ff; margin-bottom: 12px;">Search & Scrape</h4>
            <p style="color: #94a3b8; font-size: 0.95rem;">Scours web & databases for latest energy research</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div style="background: rgba(0, 212, 255, 0.1); border: 1px solid rgba(0, 212, 255, 0.3); border-radius: 12px; padding: 20px; text-align: center; animation: fadeInUp 0.7s ease-out;">
            <h3 style="color: #00d4ff; margin-top: 0;">🧠</h3>
            <h4 style="color: #0099ff; margin-bottom: 12px;">Analyze & Extract</h4>
            <p style="color: #94a3b8; font-size: 0.95rem;">AI identifies and prioritizes key findings</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div style="background: rgba(0, 212, 255, 0.1); border: 1px solid rgba(0, 212, 255, 0.3); border-radius: 12px; padding: 20px; text-align: center; animation: fadeInUp 0.8s ease-out;">
            <h3 style="color: #00d4ff; margin-top: 0;">📝</h3>
            <h4 style="color: #0099ff; margin-bottom: 12px;">Synthesize & Report</h4>
            <p style="color: #94a3b8; font-size: 0.95rem;">Generates comprehensive, structured reports</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            """
            <div style="background: rgba(0, 212, 255, 0.1); border: 1px solid rgba(0, 212, 255, 0.3); border-radius: 12px; padding: 20px; text-align: center; animation: fadeInUp 0.9s ease-out;">
            <h3 style="color: #00d4ff; margin-top: 0;">💾</h3>
            <h4 style="color: #0099ff; margin-bottom: 12px;">Store & Retrieve</h4>
            <p style="color: #94a3b8; font-size: 0.95rem;">Saves all reports for future reference</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("- **Grid Stability & Policy**: How will 2030 renewable mandates affect grid stability?\n- **Storage Technology**: What advances in long-duration energy storage emerged in 2025?\n- **Clean Industry**: What is the role of green hydrogen in decarbonizing heavy industry?")
    with col2:
        st.markdown("- **Emerging Trends**: What are the latest trends in grid-scale battery storage?\n- **Cost Analysis**: How do solar costs compare to traditional energy sources?\n- **Implementation**: What challenges do microgrids face in rural areas?")

    st.markdown("---")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("<p style='color: #cbd5e1; font-size: 1.1rem; font-weight: 500; margin-bottom: 20px;'>Ready to explore energy insights? Start by asking your first question below.</p>", unsafe_allow_html=True)
    with col2:
        if st.button("🚀 Ask a Query"):
            st.session_state.page = "ask"
            safe_rerun()

else:
    st.markdown("<h2 style='color: #00d4ff; margin-bottom: 0.5rem;'>🔬 Energy Research Query</h2><p style='color: #94a3b8; margin-bottom: 2rem;'>Enter your energy research question below for intelligent analysis</p>", unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("<h3 style='color: #00d4ff; margin-top: 0;'>📚 Research History</h3>", unsafe_allow_html=True)
        if not st.session_state.history:
            st.info("💡 No saved searches yet. Your research will appear here!")
        else:
            for rec in st.session_state.history:
                q = rec.get("query", "")
                rid = rec.get("id")
                label = q if len(q) < 40 else q[:37] + "..."
                if st.button(f"📄 {label} ({rid})", key=f"hist_{rid}"):
                    st.session_state.last_query = q
                    st.session_state.page = "ask"
                    st.session_state.current_report = rec
                    safe_rerun()

        st.markdown("---")
        if st.button("🔄 Reload History"):
            load_history()
            safe_rerun()

    query_input = st.text_input(
        "💬 What would you like to research about energy?",
        value=st.session_state.last_query,
        placeholder="e.g., What are the latest trends in grid-scale battery storage in 2025?",
        help="Ask specific, research-focused questions about renewable energy, grid technology, storage, policy, or implementation challenges."
    )
    st.session_state.last_query = query_input

    col1, col2, col3 = st.columns([2.5, 1.5, 1])
    with col1:
        run_btn = st.button("🚀 Generate Research Report", disabled=not query_input.strip() or not backend_ok)
    with col2:
        sim_btn = st.button("🔎 Search History", disabled=not query_input.strip() or not backend_ok)
    with col3:
        if st.button("🏠 Home"):
            st.session_state.page = "home"
            safe_rerun()

    if run_btn:
        with st.spinner("🔍 Researching (searching + scraping + analyzing + summarizing)..."):
            try:
                data = _post("/research", {"query": query_input})
                st.session_state.current_report = {
                    "query": query_input,
                    "title": data["report"].get("title"),
                    "introduction": data["report"].get("introduction"),
                    "key_findings": data["report"].get("key_findings"),
                    "conclusion": data["report"].get("conclusion"),
                    "sources": data.get("sources", []),
                    "id": data.get("report_id"),
                }
                st.success(f"✅ Report saved to knowledge base.")
                load_history()
            except Exception:
                st.error("❌ Research failed. Check backend logs for details.")

    if sim_btn:
        with st.spinner("🔎 Searching knowledge base..."):
            try:
                results = _post("/similarity_search", {"query": query_input, "k": 5})
                st.markdown("<h3 style='color: #00d4ff; margin-top: 2rem;'>📚 Similar Past Reports</h3><p style='color: #94a3b8;'>Results ordered by semantic similarity to your query</p>", unsafe_allow_html=True)
                for r in results.get("results", []):
                    meta = r.get("metadata") or {}
                    st.markdown(
                        f"""
                        <div style='background: rgba(0, 212, 255, 0.05); border-left: 3px solid #00d4ff; padding: 16px; border-radius: 8px; margin-bottom: 12px;'>
                        <p style='color: #00d4ff; font-weight: 600; margin: 0 0 8px 0;'>Report ID: {meta.get('report_id')}</p>
                        <p style='color: #cbd5e1; margin: 0 0 8px 0;'><strong>Query:</strong> {meta.get('query')}</p>
                        <p style='color: #94a3b8; margin: 0;'>{r.get('content_preview') or ''}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            except Exception:
                st.error("❌ Search failed. Check backend logs for details.")

    report = st.session_state.current_report
    if report:
        st.markdown("---")
        st.markdown(f"<h2 style='color: #00d4ff; margin-top: 2rem; margin-bottom: 0.5rem;'>📋 {report.get('title', 'Report') or 'Report'}</h2><p style='color: #94a3b8; margin-bottom: 1.5rem;'><strong>Query:</strong> {report.get('query') or ''}</p>", unsafe_allow_html=True)

        intro_content = report.get('introduction', '').strip() or f"This report provides a concise introduction for your query: '{report.get('query', '')}'."
        conclusion_content = report.get('conclusion', '').strip() or f"This conclusion summarizes the outcome of your query: '{report.get('query', '')}'."

        with st.expander("📖 Introduction", expanded=True):
            st.markdown(f"<p style='color: #00d4ff; font-weight: 600; line-height: 1.8; font-size: 1.15rem; margin: 0 0 10px 0;'>{intro_content}</p>", unsafe_allow_html=True)

        with st.expander("🔑 Key Findings", expanded=True):
            findings_list = report.get('key_findings', [])
            points: List[str] = []

            if isinstance(findings_list, str):
                points = extract_key_findings(findings_list)
            elif isinstance(findings_list, list):
                combined = '\n'.join(str(x) for x in findings_list if x)
                points = extract_key_findings(combined)

            if not points:
                st.info('No key findings available for this report. Try re-running or refining your query.')
            else:
                for idx, point in enumerate(points, 1):
                    st.markdown(
                        f"""
                        <div style='background: rgba(0, 212, 255, 0.08); border-left: 4px solid #00d4ff; padding: 16px; border-radius: 8px; margin-bottom: 14px; word-wrap: break-word; overflow-wrap: break-word; white-space: normal;'>
                        <p style='color: #00d4ff; font-weight: 700; margin: 0 0 8px 0; font-size: 1.15rem;'>• {point}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        with st.expander('✅ Conclusion', expanded=True):
            st.markdown(f"<p style='color: #00d4ff; font-weight: 600; line-height: 1.8; font-size: 1.15rem; margin: 0;'>{conclusion_content}</p>", unsafe_allow_html=True)

        st.markdown("<h3 style='color: #0099ff; margin-top: 2rem; margin-bottom: 1rem;'>🔗 Sources & References</h3>", unsafe_allow_html=True)
        for idx, s in enumerate(report.get('sources', []), 1):
            title = s.get('title') or s.get('url')
            url = s.get('url')
            st.markdown(
                f"""
                <div style='background: rgba(0, 212, 255, 0.05); border: 1px solid rgba(0, 212, 255, 0.2); padding: 12px 16px; border-radius: 8px; margin-bottom: 12px;'>
                <p style='margin: 0 0 8px 0; color: #00d4ff; font-weight: 600;'>📌 Source {idx}</p>
                <p style='margin: 0;'><a href='{url}' target='_blank' style='color: #0099ff; text-decoration: none; font-weight: 500; word-break: break-all;'>{title}</a></p>
                </div>
                """,
                unsafe_allow_html=True,
            )

