from __future__ import annotations

import logging
import os
from typing import Optional

from config.settings import settings

logger = logging.getLogger(__name__)


def _build_groq_llm():
    """
    Groq API - Fastest inference with free tier.
    Get API key from: https://console.groq.com
    """
    from langchain_groq import ChatGroq

    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "❌ GROQ_API_KEY not found in .env file!\n"
            "   1. Go to https://console.groq.com\n"
            "   2. Sign up (free)\n"
            "   3. Create an API key\n"
            "   4. Add to .env: GROQ_API_KEY=your_key_here"
        )
    
    model_name = os.getenv("GROQ_MODEL", "llama3-70b-8192").strip()
    logger.info(f"🚀 Using Groq API with model: {model_name}")
    
    return ChatGroq(
        model=model_name,
        api_key=api_key,
        temperature=0.7,
        max_tokens=1024,
    )


def _build_huggingface_pipeline():
    # Local, open-source model via transformers pipeline.
    # Note: flan-t5-base is lightweight and CPU-friendly (relative to 7B models).
    from transformers import pipeline

    device = -1  # CPU by default
    # Users with CUDA can set HF_DEVICE=0 etc.
    env_device = os.getenv("HF_DEVICE")
    if env_device is not None:
        try:
            device = int(env_device)
        except ValueError:
            device = -1

    generator = pipeline(
        task="text-generation",
        model=os.getenv("HF_MODEL_NAME", settings.hf_model_name),
        device=device,
        max_new_tokens=int(os.getenv("HF_MAX_NEW_TOKENS", "800")),
    )
    return generator


def _build_langchain_llm_from_hf_pipeline():
    from langchain_huggingface import HuggingFacePipeline

    hf_pipe = _build_huggingface_pipeline()
    return HuggingFacePipeline(pipeline=hf_pipe)


def _build_langchain_llm_from_ollama(model_name: Optional[str] = None):
    # Ollama is fully local (free). Requires Ollama installed and running.
    from langchain_community.llms import Ollama

    return Ollama(model=model_name or os.getenv("OLLAMA_MODEL_NAME", settings.ollama_model_name))


def get_llm():
    """
    Get LLM in priority order:
    1. Groq (fastest, requires API key)
    2. Ollama (local, requires Ollama running)
    3. HuggingFace (local, works on CPU)
    """
    provider = os.getenv("LLM_PROVIDER", settings.llm_provider).strip().lower()
    
    # Try Groq first (fastest)
    if provider == "groq":
        try:
            logger.info("🚀 Using Groq API (fastest!)")
            return _build_groq_llm()
        except Exception as e:
            logger.warning(f"Groq failed: {e}. Falling back to HuggingFace...")
            logger.info("💻 Using HuggingFace (local CPU model)")
            return _build_langchain_llm_from_hf_pipeline()
    
    # Try Ollama
    elif provider == "ollama":
        logger.info("📦 Using Ollama (local model)")
        return _build_langchain_llm_from_ollama()
    
    # Default to HuggingFace
    else:
        logger.info("💻 Using HuggingFace (local CPU model)")
        return _build_langchain_llm_from_hf_pipeline()
