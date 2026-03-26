

# Autonomous Energy Researcher Agent

An **LLM-powered multi-agent research system** that automatically researches energy-related topics using AI agents, analyzes the data, generates a structured report, and stores it in a local FAISS knowledge base.

The system supports **Groq (Llama 3.1)** for fast responses and also works **offline using HuggingFace models** as a fallback.

---

## System Workflow

User Query
→ Research Agent (search + scrape web data)
→ Analysis Agent (filters & structures content)
→ Summary Agent (generates final research report)
→ FAISS Knowledge Base (stores embeddings)
→ Streamlit Web UI

---

## Tech Stack 

### Programming Language

* Python

### LLM / AI Models

* **Groq API (Primary Model)**

  * `llama-3.1-8b-instant` (very fast and free tier supported)

* **HuggingFace (Fallback Model)**

  * `google/flan-t5-base` (runs locally without internet)

* Optional:

  * Ollama (fully offline LLM support)

---

### Embeddings

* `sentence-transformers/all-MiniLM-L6-v2`

---

### Web Research Tools

* DuckDuckGo Search (free)
* Selenium (dynamic website scraping)
* BeautifulSoup (fallback scraper)

---

### Backend

* FastAPI

### Frontend

* Streamlit

### Database / Storage

* FAISS (local vector database)
* JSON file storage for reports

---

## Environment Configuration (.env)

Create a `.env` file in the project root and add:

```env
# -------------------------------
# Primary Model (Groq - Fastest)
# -------------------------------
GROQ_MODEL=llama-3.1-8b-instant

# -------------------------------
# HuggingFace Fallback Model
# -------------------------------
HF_MODEL_NAME=google/flan-t5-base
HF_DEVICE=-1
HF_MAX_NEW_TOKENS=800

# -------------------------------
# Optional: Ollama (local models)
# -------------------------------
# OLLAMA_MODEL_NAME=mistral

# -------------------------------
# Scraper Configuration
# -------------------------------
SELENIUM_HEADLESS=true
SELENIUM_PAGE_LOAD_TIMEOUT=25
REQUEST_TIMEOUT=20
MAX_SEARCH_RESULTS=1
MAX_CHARS_PER_PAGE=500
```

---

## Project Folder Structure

```
AUTONOMOUS ENERGY RESEARCHER AGENT
│
├── backend
│   ├── main.py
│   ├── pipeline.py
│   ├── agents
│   │   ├── research_agent.py
│   │   ├── analysis_agent.py
│   │   └── summary_agent.py
│
├── database
│   ├── faiss_store.py
│   └── storage.py
│
├── data
│   ├── faiss
│   └── reports
│
├── frontend
│   ├── app.py
│   └── styles.py
│
├── config
├── models
├── tools
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Installation (Windows / PowerShell)

### Step 1: Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

```bash
.\.venv\Scripts\activate
```

---

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run the Backend (FastAPI)

```bash
uvicorn backend.main:app --reload --port 8000
```

Test API:

```
http://127.0.0.1:8000/health
```

---

## Run the Frontend (Streamlit)

Open another terminal:

```bash
streamlit run frontend/app.py
```

---

## Features

* Multi-agent research system (Research + Analysis + Summary agents)
* Fast responses using Groq (Llama 3.1)
* Works offline using HuggingFace fallback model
* Automatic report generation
* Local FAISS vector database
* Similarity search for previous research
* Streamlit-based interactive UI
* Fully free tools (no paid APIs required)

---

## What Gets Stored Locally

The system automatically stores:

```
data/reports/     → Generated research reports
data/faiss/       → Vector embeddings database
```

These folders are **not uploaded to GitHub** (already ignored in `.gitignore`).

---

## API Endpoints

### Generate Research

```
POST /research
```

Example:

```json
{
  "query": "Future of renewable energy in India"
}
```

---

### Get Previous Reports

```
GET /reports?limit=20
```

---

### Similarity Search

```
POST /similarity_search
```

Example:

```json
{
  "query": "solar power trends",
  "k": 5
}
```

---

## Author

Final Year AI/ML Project
**Autonomous Energy Researcher Agent**

---

If you want, I can also give you:

* a **short 5-line project description** (for GitHub Classroom submission), and
* a **perfect .gitignore for AI projects**.


