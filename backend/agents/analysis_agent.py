from __future__ import annotations

import logging
import re
from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from langchain_core.language_models.base import BaseLanguageModel

logger = logging.getLogger(__name__)


@dataclass
class AnalysisOutput:
    query: str
    cleaned_corpus: str
    key_points: List[str]


class AnalysisAgent:
    """
    Responsibilities:
    - Remove irrelevant data / boilerplate
    - Extract key insights into structured points
    """

    def __init__(self, llm: BaseLanguageModel):
        self.llm = llm

    def _light_clean(self, text: str) -> str:
        # Keep it conservative; the LLM will do the heavy lifting.
        text = re.sub(r"\b(cookie|cookies|subscribe|sign up|newsletter|accept all)\b", " ", text, flags=re.I)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def _summarize_content(self, query: str, content: str) -> str:
        """Summarize long content to fit within token limits."""
        summary_prompt = (
            f"Summarize this web content relevant to the query: {query}\n\n"
            f"CONTENT:\n{content[:10000]}\n\n"  # Take first 10K chars
            "Provide a concise summary (max 1000 words) focusing on key facts and information:"
        )
        
        logger.info("📝 Summarizing content for analysis...")
        try:
            resp = self.llm.invoke(summary_prompt)
            summary = resp if isinstance(resp, str) else str(resp)
            return summary[:2000]  # Limit summary length
        except Exception as e:
            logger.warning(f"❌ Summarization failed: {e}. Using truncated content.")
            return content[:1500]  # Fallback to truncation

    def run(self, query: str, raw_corpus: str) -> AnalysisOutput:
        logger.info(f"🔬 Starting analysis for query: {query}")
        logger.info(f"📄 Raw corpus length: {len(raw_corpus)} characters")
        
        if not raw_corpus.strip():
            logger.error("🚨 Empty corpus received! Analysis will fail.")
            return AnalysisOutput(
                query=query, 
                cleaned_corpus="", 
                key_points=["No content was found to analyze. Please try a different search query."]
            )
        
        cleaned = self._light_clean(raw_corpus)
        logger.info(f"🧹 After cleaning: {len(cleaned)} characters")
        
        # If content is too long, summarize it first
        if len(cleaned) > 2000:
            logger.info("📝 Content too long, summarizing first...")
            cleaned = self._summarize_content(query, cleaned)
            logger.info(f"📋 After summarization: {len(cleaned)} characters")
        
        # Keep prompt much shorter now
        prompt = (
            f"Analyze this content for the query: {query}\n\n"
            f"CONTENT:\n{cleaned}\n\n"
            "Extract 5-8 key bullet points (1-2 sentences each):"
        )

        logger.info("🤖 Calling LLM for analysis...")
        resp = self.llm.invoke(prompt)
        text = resp if isinstance(resp, str) else str(resp)
        logger.info(f"📝 LLM response length: {len(text)} characters")
        
        bullets = self._parse_bullets(text)
        logger.info(f"✅ Extracted {len(bullets)} key points")

        # If the model didn't behave, degrade gracefully.
        if not bullets:
            logger.warning("⚠️  No bullets extracted from LLM response")
            bullets = ["Unable to extract structured key points from the sources reliably. Please refine the query."]

        return AnalysisOutput(query=query, cleaned_corpus=cleaned, key_points=bullets)

    def _parse_bullets(self, text: str) -> List[str]:
        """Parse bullet points from LLM response, handling various formats."""
        # Split by common separators
        text = text.replace("\n* ", "|||").replace("\n- ", "|||").replace("\n• ", "|||")
        text = re.sub(r"\n\d+\.\s+", "|||", text)
        
        bullets = text.split("|||")
        out: List[str] = []
        
        for bullet in bullets:
            bullet = bullet.strip()
            bulletin = re.sub(r"^[\-\*\u2022]\s*", "", bullet)
            bullet = re.sub(r"^\d+\.\s*", "", bullet)
            
            # Remove 'content=' prefix if present
            if bullet.startswith("content='") or bullet.startswith("content=\""):
                bullet = bullet[9:]
            if bullet.endswith("'") or bullet.endswith('"'):
                bullet = bullet[:-1]
            
            bullet = bullet.strip().replace("\\n", " ").replace("\\n*", " ")
            
            if len(bullet) < 5 or not bullet:
                continue
            if len(bullet) > 400:
                bullet = bullet[:400].rsplit(' ', 1)[0]
            
            out.append(bullet)
        
        return out[:12] if out else []

    def to_dict(self, output: AnalysisOutput) -> Dict[str, Any]:
        return asdict(output)
