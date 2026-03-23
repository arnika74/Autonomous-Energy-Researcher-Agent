# QUICK START - Run Your Project in 5 Steps

## Step 1: Install Dependencies (First Time Only)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Step 2: Start Backend (Terminal 1)
```powershell
.\.venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload --port 8000
```

👉 **Look for this message:**
```
✅ Backend initialized successfully!
📡 Connected components: ResearchPipeline, Knowledge Base, LocalStorage
🚀 Backend is running and ready to receive requests from frontend
```

## Step 3: Start Frontend (Terminal 2)
```powershell
.\.venv\Scripts\Activate.ps1
streamlit run frontend/app.py
```

👉 **Look for this message:**
```
✅ Connected to backend at http://127.0.0.1:8000
```

## Step 4: Ask a Question
1. Go to Streamlit URL (usually `http://localhost:8501`)
2. Type your question in the text box
3. Click "Generate Research"
4. Wait for results

## Step 5: Verify Connection Works
When you submit a query, check **Backend Terminal 1** for this line:
```
💾 Report saved with ID: 1234567890
```

👈 **This line confirms your backend is working!**

---

## What Each Message Means

| Message | Location | Meaning |
|---------|----------|---------|
| `✅ Backend initialized successfully!` | Backend at startup | Backend is ready |
| `📡 Connected components: ...` | Backend at startup | All parts are connected |
| `🚀 Backend is running and ready...` | Backend at startup | Ready to receive requests |
| `✅ Connected to backend at ...` | Frontend at startup | Frontend found backend |
| `🔍 Received research query:` | Backend when you click button | Your question was received |
| `✅ Research completed successfully` | Backend after processing | Pipeline finished |
| `💾 Report saved with ID:` | Backend when saving | Data was saved **← CHECK THIS!** |
| `✅ Found X similar documents` | Backend on similarity search | Knowledge base search worked |

---

## .env File Details

Located in: **Project root folder**

**What's in it:**
- `BACKEND_URL=http://127.0.0.1:8000` - Where frontend finds backend
- `LLM_PROVIDER=huggingface` - Using free HuggingFace model
- `HF_MODEL_NAME=google/flan-t5-base` - Free small model
- `HF_DEVICE=-1` - Use CPU (no GPU needed)

**Do you need API keys/tokens?** 
- ❌ NO! Everything is free and open-source

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Cannot connect to backend" | Backend not running? Check Terminal 1 |
| "Research failed" | Check Terminal 1 for error message |
| "No stored reports" | Normal on first run - generate reports first |
| Backend not showing status | Check if messages appear after startup |
| Frontend won't load | Check if backend is running first |

---

## File Changes Made

### Backend (`backend/main.py`)
- ✅ Added CORS (allows frontend to connect)
- ✅ Added startup messages (shows it's running)
- ✅ Added logging (shows what's happening)
- ✅ Added error handling (catches errors)

### Frontend (`frontend/app.py`)  
- ✅ Added connection check (verifies backend is running)
- ✅ Better error messages (tells you what went wrong)
- ✅ Handles all errors gracefully

### Configuration
- ✅ Created `.env` file (stores settings)
- ✅ Updated `config/settings.py` (loads .env)

### Documentation
- ✅ `SETUP_INSTRUCTIONS.md` - How to set up
- ✅ `CHANGES.md` - What was changed and why
- ✅ `VERIFICATION.md` - Checklist and details
- ✅ `QUICK_START.md` - This file!

---

## Summary of Your Project

```
User Types Question
    ↓
Frontend (Streamlit) sends to Backend (FastAPI)
    ↓
Backend receives (🔍 log message)
    ↓
Research Agent (DuckDuckGo search)
    ↓
Analysis Agent (AI analysis)
    ↓
Summary Agent (Generates report)
    ↓
Saves to Database (💾 log message ← This confirms it works!)
    ↓
Saves to FAISS (Knowledge base)
    ↓
Returns to Frontend
    ↓
User sees results with sources
```

---

## Key Connection Line to Monitor

When you submit a research query, watch for this in Terminal 1:
```
💾 Report saved with ID: 1234567890
```

**If you see this line = SUCCESS! ✅**

---

## Everything You Need to Know is Ready! 🚀

Your project is now:
- ✅ Fully connected (backend ↔ frontend)
- ✅ Showing status (startup messages)
- ✅ Logging everything (monitor progress)
- ✅ Configured (.env file created)
- ✅ Documented (3 guide files created)

**Now just run it and enjoy!**
