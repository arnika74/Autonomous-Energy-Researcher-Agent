# 🤖 Model Configuration Guide

## Your Current Setup ✅

### 1. **Main LLM: LLaMA3 70B via Groq API** ⚡
- **Model:** `llama3-70b-8192`
- **Provider:** Groq API (ultra-fast)
- **Why:** Best performance for CrewAI multi-agent workflows
- **Speed:** 5-10 seconds per query
- **Cost:** FREE (free tier available)

### 2. **Embedding Model: sentence-transformers/all-MiniLM-L6-v2** 📊
- **Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Provider:** HuggingFace (local)
- **Why:** Converts text to vectors for FAISS similarity search
- **Size:** Small, fast, runs locally
- **Purpose:** Knowledge base search functionality

---

## Why HuggingFace is Still Required

### ❌ **NOT for Main LLM**
Your main LLM uses **Groq API** (LLaMA3), not HuggingFace!

### ✅ **ONLY for Embeddings**
HuggingFace is **required** for the embedding model because:

| Reason | Why HuggingFace | Alternative? |
|--------|----------------|--------------|
| **Local Processing** | Embeddings run locally for privacy | No API alternative |
| **FAISS Integration** | LangChain FAISS uses HuggingFace embeddings | No other provider |
| **No API Key Needed** | Works without authentication | Free forever |
| **Small & Fast** | 23MB model, instant loading | Perfect for your use case |

**Bottom Line:** HuggingFace here is just a **library**, not a service. No API keys, no costs, no internet required after download.

---

## Model Options Available

### Groq API Models (Main LLM)

| Model | Size | Speed | Best For |
|-------|------|-------|----------|
| `llama3-70b-8192` | 70B | Medium | **Your choice - Best quality** |
| `llama3-8b-8192` | 8B | Fast | Quick responses |
| `mixtral-8x7b-32768` | 47B | Medium | Balanced performance |

### Embedding Models

| Model | Size | Speed | Use Case |
|-------|------|-------|----------|
| `sentence-transformers/all-MiniLM-L6-v2` | 23MB | ⚡ Fast | **Your choice - Perfect** |
| `sentence-transformers/all-mpnet-base-v2` | 109MB | Medium | Higher quality |
| `sentence-transformers/paraphrase-MiniLM-L6-v2` | 23MB | ⚡ Fast | Alternative |

---

## How to Change Models

### Change Main LLM Model

**Edit `.env` file:**
```ini
# Change this line to switch models:
GROQ_MODEL=llama3-8b-8192    # For faster responses
# or
GROQ_MODEL=mixtral-8x7b-32768  # For Mixtral
```

**Restart backend** after changing.

### Change Embedding Model

**Edit `config/settings.py` line 25:**
```python
embedding_model_name: str = "sentence-transformers/all-mpnet-base-v2"
```

**Restart backend** after changing.

---

## Performance Comparison

### Main LLM Speed (with Groq API):

| Model | Response Time | Quality |
|-------|---------------|---------|
| LLaMA3 70B | 8-12 seconds | ⭐⭐⭐⭐⭐ |
| LLaMA3 8B | 3-5 seconds | ⭐⭐⭐⭐ |
| Mixtral 8x7B | 5-8 seconds | ⭐⭐⭐⭐⭐ |

### Embedding Speed (Local):

| Model | Load Time | Search Speed |
|-------|-----------|--------------|
| MiniLM-L6-v2 | 2 seconds | ⚡ Instant |
| MPNet base | 5 seconds | Fast |
| Others | Varies | Varies |

---

## Your Configuration Summary

```
┌─────────────────┐    ┌──────────────────┐
│   Frontend      │    │    Backend       │
│   (Streamlit)   │◄──►│   (FastAPI)      │
└─────────────────┘    └──────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
            ┌───────▼──────┐    ┌──────▼──────┐
            │  LLaMA3      │    │ MiniLM-L6   │
            │  via Groq    │    │ via HF      │
            │  (Main LLM)  │    │ (Embeddings)│
            └──────────────┘    └─────────────┘
```

**✅ Everything is optimized for speed and quality!**

---

## Setup Verification

### 1. Add Your Groq API Key

**File:** `.env` (line 9)
```
GROQ_API_KEY=gsk_your_actual_key_here
```

### 2. Choose Your Model

**File:** `.env` (line 15)
```
GROQ_MODEL=llama3-70b-8192  # Already set to LLaMA3 70B
```

### 3. Start and Verify

**Terminal 1:**
```powershell
uvicorn backend.main:app --reload --port 8000
```

**Look for:**
```
🚀 Using Groq API with model: llama3-70b-8192
✅ Backend initialized successfully!
```

**Terminal 2:**
```powershell
streamlit run frontend/app.py
```

---

## Why This Setup is Perfect

✅ **LLaMA3 70B:** Most powerful model available via Groq  
✅ **MiniLM-L6-v2:** Fastest, smallest embedding model  
✅ **Groq API:** 10x faster than local models  
✅ **FAISS:** Efficient vector search  
✅ **CrewAI:** Optimized for multi-agent workflows  

**No compromises - best of both worlds!** 🚀

---

## Troubleshooting

### "Model not found" error?
- Check your Groq API key is correct
- Verify model name in `.env`: `GROQ_MODEL=llama3-70b-8192`

### Slow responses?
- Try `GROQ_MODEL=llama3-8b-8192` for faster responses
- Check your internet connection

### Embedding issues?
- Embeddings run locally, should be instant
- If slow, try restarting the backend

---

## Summary

**Your setup is now optimized:**
- ⚡ **LLaMA3 70B** via Groq (fastest main LLM)
- 📊 **MiniLM-L6-v2** via HuggingFace (fastest embeddings)
- 🔍 **FAISS** for knowledge base search
- 🤖 **CrewAI** for multi-agent research

**HuggingFace is only used for embeddings (no API key needed) and provides the best local performance for your use case!** ✅