# Autonomous Energy Researcher Agent

An offline-friendly, **free/open-source** multi-agent research system that:

User Query → Research Agent → Analysis Agent → Summary Agent → Knowledge Repository (FAISS) → Web UI

## Tech stack (free only)

- **Python**
- **LangChain** + **CrewAI**
- **Local LLM**:
  - Default: HuggingFace `google/flan-t5-base` (runs locally)
  - Optional: Ollama local model (also fully local)
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- **Web search**: DuckDuckGo (free) via `ddgs`
- **Web scraping**: Selenium (dynamic) + BeautifulSoup fallback
- **Vector DB**: FAISS (local)
- **Backend**: FastAPI
- **Frontend**: Streamlit

## Folder structure

```
backend/
  main.py
  pipeline.py
  agents/
    research_agent.py
    analysis_agent.py
    summary_agent.py
tools/
  search_tool.py
  scraper_tool.py
  embedding_tool.py
database/
  faiss_store.py
  storage.py
frontend/
  app.py
models/
  llm_model.py
config/
  settings.py
requirements.txt
README.md
```

## Setup (Windows / PowerShell)

Create a virtual env and install deps:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run the backend (FastAPI)

```bash
uvicorn backend.main:app --reload --port 8000
```

Health check: `http://127.0.0.1:8000/health`

## Run the frontend (Streamlit)

In a second terminal (same venv):

```bash
streamlit run frontend/app.py
```

## Selenium notes (important)

This project **tries Selenium first**, then falls back to `requests + BeautifulSoup` if Selenium fails.

To enable Selenium scraping reliably, you need a WebDriver installed and available on your PATH:

- **Chrome**: install a matching `chromedriver.exe`
- Or use Firefox with `geckodriver.exe` (you’d need to update the scraper to Firefox if desired)

If you don’t install a driver, the system will still work via the fallback scraper, but may fail on heavily dynamic sites.

## Switching the LLM (optional)

### Option A: HuggingFace (default)

Uses `google/flan-t5-base` locally.

You can override the model name:

```bash
setx HF_MODEL_NAME "google/flan-t5-base"
```

### Option B: Ollama (fully local)

1) Install Ollama and pull a model:

```bash
ollama pull mistral
```

2) Set provider:

```bash
setx LLM_PROVIDER "ollama"
setx OLLAMA_MODEL_NAME "mistral"
```

Restart terminals after `setx`.

## What gets stored

- **Reports**: `data/reports/*.json` and `*.txt`
- **FAISS index**: `data/faiss/index/` (persisted)

The Streamlit UI can:

- Generate a new research report
- Show sources used
- Query the FAISS knowledge base for similar past reports
- List previously saved reports

## API endpoints

- `POST /research` body: `{ "query": "..." }`
- `GET /reports?limit=20`
- `POST /similarity_search` body: `{ "query": "...", "k": 5 }`

