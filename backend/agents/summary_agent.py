from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from langchain_core.language_models.base import BaseLanguageModel

logger = logging.getLogger(__name__)


@dataclass
class SummaryReport:
    title: str
    introduction: str
    key_findings: List[str]
    conclusion: str


class SummaryAgent:
    """
    Responsibilities:
    - Use local LLM to generate a structured report:
      Title, Introduction, Key Findings, Conclusion
    """

    def __init__(self, llm: BaseLanguageModel):
        self.llm = llm

    def run(self, query: str, key_points: List[str]) -> SummaryReport:
        logger.info(f"📋 Starting summary generation for query: {query}")
        logger.info(f"📝 Received {len(key_points)} key points")
        
        if not key_points:
            logger.error("🚨 No key points received! Summary will fail.")
            return SummaryReport(
                title=f"Research Summary: {query[:80]}",
                introduction="No key points were available to generate a summary.",
                key_findings=["No analysis results were generated."],
                conclusion="Please try a different search query or check the search results."
            )
        
        key_points_text = "\n".join([f"- {k}" for k in key_points])

        prompt = (
            f"Query: {query}\n\n"
            f"Key findings:\n{key_points_text}\n\n"
            "You are a summarization engine. Produce a complete structured report with clear full sentences and no incomplete fragments. "
            "Always include all sections. If output is interrupted/truncated, begin the next response with CONTINUE and carry on.\n\n"
            "Write report as JSON only (no markdown, no extra text):\n"
            "{\n"
            '"title":"<short title>",\n'
            '"introduction":"<2-3 sentence introduction>",\n'
            '"key_findings":["<full point 1>","<full point 2>","<full point 3>"],\n'
            '"conclusion":"<2-3 sentence conclusion>"\n'
            "}"
        )

        logger.info("🤖 Calling LLM for summary generation...")
        resp = self.llm.invoke(prompt)
        text = resp if isinstance(resp, str) else str(resp)
        logger.info(f"📄 LLM summary response length: {len(text)} characters")

        parsed = self._safe_parse_json(text)
        if parsed is None:
            logger.warning("⚠️  Failed to parse JSON from LLM response, using fallback")
            # Fallback: properly format key_points as separate findings
            formatted_findings = []
            for point in key_points[:12]:
                point_str = str(point).strip()
                # Remove any weird prefixes/suffixes
                if point_str.startswith("content='"):
                    point_str = point_str[9:]
                if point_str.endswith("'"):
                    point_str = point_str[:-1]
                # Clean up escaped newlines
                point_str = point_str.replace("\\n", " ").replace("\\n*", " ").strip()
                if len(point_str) > 400:
                    point_str = point_str[:400]
                if point_str:
                    formatted_findings.append(point_str)
            
            return SummaryReport(
                title=f"Research Summary: {query[:80]}",
                introduction="This report summarizes key information gathered from recent web sources relevant to your energy research query.",
                key_findings=formatted_findings if formatted_findings else ["No structured findings were extracted."],
                conclusion="For more accurate information, validate key claims and numbers against official sources and primary research datasets.",
            )

        logger.info("✅ Successfully generated structured report")

        return SummaryReport(
            title=str(parsed.get("title") or f"Research Summary: {query[:80]}"),
            introduction=str(parsed.get("introduction") or "").strip(),
            key_findings=[str(x).strip() for x in (parsed.get("key_findings") or []) if str(x).strip()],
            conclusion=str(parsed.get("conclusion") or "").strip(),
        )

    def _safe_parse_json(self, text: str) -> Dict[str, Any] | None:
        # Try to extract the first JSON object from the model output.
        # Remove markdown code blocks if present
        text = text.replace("```json", "").replace("```", "")
        
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return None
        
        candidate = text[start : end + 1].strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            return None

    def to_dict(self, report: SummaryReport) -> Dict[str, Any]:
        return asdict(report)
