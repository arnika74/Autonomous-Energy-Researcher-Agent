# 🚀 Groq API Setup Guide

## What is Groq?

Groq is a **FREE** API that provides ultra-fast inference. Perfect for CrewAI and LLM applications.
- ⚡ **10x faster** than local models
- 💰 **Free tier** available
- 🔑 **Easy setup** (just an API key)
- ✅ **Works perfectly** with CrewAI

---

## Step-by-Step Setup

### Step 1: Get Your Groq API Key

1. **Go to:** https://console.groq.com
2. **Click:** "Sign Up" (free, no credit card needed)
3. **Create account** with email
4. **Once logged in** → Click on "API Keys" in left sidebar
5. **Click:** "Create New API Key"
6. **Copy the key** (it looks like: `gsk_xxxxxxxxxxxxxxxxxxxx`)

**⚠️ Keep this key SECRET** - Don't share it with anyone!

---

### Step 2: Add Key to .env File

**File location:** `c:\Users\jaina\Downloads\Autonomous Energy Researcher Agent\.env`

**Find this line:**
```
GROQ_API_KEY=your_groq_api_key_here
```

**Replace `your_groq_api_key_here` with your actual key:**
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

**Example (fake key):**
```
GROQ_API_KEY=gsk_7B9mK2pLqR8wNxYzAbC1DeFgHiJkLmNoPqRsTuVwXyZ
```

---

### Step 3: Verify Configuration

Your `.env` file should look like:
```ini
# Backend Configuration
BACKEND_URL=http://127.0.0.1:8000

# LLM Configuration
LLM_PROVIDER=groq

# Groq API Configuration
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx

# ... rest of config
```

---

## Step 4: Install Updated Packages

Run this in your terminal:
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

This installs `langchain-groq` (the integration layer).

---

## Step 5: Start Your Project

### Terminal 1 - Backend:
```powershell
.\.venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload --port 8000
```

**Look for this message:**
```
🚀 Using Groq API (fastest!)
```

### Terminal 2 - Frontend:
```powershell
.\.venv\Scripts\Activate.ps1
streamlit run frontend/app.py
```

---

## How to Know It's Working

### In Backend Terminal (Terminal 1), you should see:
```
🚀 Using Groq API (fastest!)
✅ Backend initialized successfully!
📡 Connected components: ResearchPipeline, Knowledge Base, LocalStorage
🚀 Backend is running and ready to receive requests from frontend
```

### When you ask a question, you'll see:
```
🔍 Received research query: What are latest trends in...
✅ Research completed successfully (MUCH FASTER NOW!)
💾 Report saved with ID: 1234567890
```

---

## Groq Models Available (Free Tier)

Your code uses: `llama3-70b-8192` (LLaMA3 70B - Most powerful)

Other available models:
- `llama3-8b-8192` - LLaMA3 8B (faster, smaller)
- `mixtral-8x7b-32768` - Mixtral (good balance)
- `gemma-7b-it` - Gemma (alternative)

---

## Troubleshooting

### Error: "GROQ_API_KEY not found"
**Solution:** Make sure you:
1. ✅ Got API key from https://console.groq.com
2. ✅ Added it to `.env` file with correct name: `GROQ_API_KEY=...`
3. ✅ Restarted your backend (stop and start again)

### Error: "Invalid API key"
**Solution:**
1. Check you copied the ENTIRE key correctly
2. Regenerate key at https://console.groq.com and try again

### Error: "Rate limit exceeded"
**Solution:** Groq's free tier has rate limits. Just wait a minute and try again.

### Want to switch back to HuggingFace?
**Solution:** Edit `.env` and change:
```
LLM_PROVIDER=huggingface
```

---

## Files Modified

| File | Change | Why |
|------|--------|-----|
| `.env` | Added `GROQ_API_KEY=...` | Stores your API key |
| `.env` | Changed `LLM_PROVIDER=groq` | Use Groq instead of HuggingFace |
| `models/llm_model.py` | Added Groq support | Connects to Groq API |
| `requirements.txt` | Added `langchain-groq` | Enables Groq integration |

---

## Why Groq is Better for CrewAI

✅ **Speed:** 10x faster than local models  
✅ **Quality:** Better responses than CPU models  
✅ **Cost:** FREE (free tier available)  
✅ **Reliability:** No GPU needed, runs on Groq servers  
✅ **CrewAI Compatible:** Perfect for multi-agent workflows  

---

## Important Notes

⚡ **Groq is WAY faster:**
- HuggingFace: 30-60 seconds per query (on CPU)
- Groq: 5-10 seconds per query (via API)

🔒 **Your API key is private:**
- Never commit `.env` file to Git
- Never share your key
- If key is leaked, regenerate it immediately

💰 **Free tier limits:**
- Groq free tier has rate limits
- But enough for development and testing
- Paid tiers available if you need more

---

## Next Steps

1. **Get API key** from https://console.groq.com
2. **Add to `.env` file** (replace `your_groq_api_key_here`)
3. **Run:** `pip install -r requirements.txt` (to get langchain-groq)
4. **Start backend:** Watch for "🚀 Using Groq API" message
5. **Enjoy FAST responses!** ⚡

---

## Summary

✅ Groq API set up for ultra-fast inference  
✅ Free tier available (no credit card)  
✅ 10x faster than local CPU models  
✅ Perfect for CrewAI multi-agent workflows  
✅ Your project is now optimized for speed! 🚀
