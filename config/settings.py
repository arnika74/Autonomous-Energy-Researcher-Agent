from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass(frozen=True)
class Settings:
    project_root: Path = Path(__file__).resolve().parents[1]

    # Storage locations
    data_dir: Path = project_root / "data"
    reports_dir: Path = data_dir / "reports"
    faiss_dir: Path = data_dir / "faiss"

    # Models
    llm_provider: str = "huggingface"  # "huggingface" or "ollama"
    hf_model_name: str = "google/flan-t5-base"
    ollama_model_name: str = "mistral"  # requires local Ollama if used
    embedding_model_name: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Research
    max_search_results: int = 8
    max_chars_per_page: int = 25_000
    request_timeout_s: int = 20

    # Selenium (optional; requires a compatible WebDriver on PATH)
    selenium_headless: bool = True
    selenium_page_load_timeout_s: int = 25


settings = Settings()
