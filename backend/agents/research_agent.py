from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from tools.scraper_tool import ScrapedPage, WebScraperTool
from tools.search_tool import DuckDuckGoSearchTool

logger = logging.getLogger(__name__)


@dataclass
class ResearchOutput:
    query: str
    sources: List[Dict[str, Any]]
    raw_corpus: str


class ResearchAgent:
    """
    Responsibilities:
    - DuckDuckGo search
    - Collect top URLs
    - Scrape and clean text from pages
    """

    def __init__(self, search_tool: DuckDuckGoSearchTool | None = None, scraper_tool: WebScraperTool | None = None):
        self.search_tool = search_tool or DuckDuckGoSearchTool()
        self.scraper_tool = scraper_tool or WebScraperTool()

    def run(self, query: str) -> ResearchOutput:
        logger.info(f"🔎 Starting search for query: {query}")
        results = self.search_tool.search(query)
        logger.info(f"📊 Found {len(results)} search results")

        sources: List[Dict[str, Any]] = []
        corpus_parts: List[str] = []

        for i, r in enumerate(results):
            logger.info(f"🌐 Scraping result {i+1}/{len(results)}: {r.url[:50]}...")
            try:
                page: ScrapedPage = self.scraper_tool.scrape(r.url)
                if not page.text or len(page.text) < 200:
                    logger.warning(f"⚠️  Page too short or empty: {r.url} ({len(page.text) if page.text else 0} chars)")
                    continue
                sources.append(
                    {
                        "title": page.title or r.title,
                        "url": page.url,
                        "snippet": r.snippet,
                        "chars": len(page.text),
                    }
                )
                corpus_parts.append(f"SOURCE: {page.url}\nTITLE: {page.title or r.title}\nCONTENT:\n{page.text}\n")
                logger.info(f"✅ Successfully scraped: {page.title or r.title} ({len(page.text)} chars)")
            except Exception as e:
                logger.error(f"❌ Failed to scrape {r.url}: {str(e)}")
                continue

        raw_corpus = "\n\n".join(corpus_parts)
        logger.info(f"📝 Final corpus: {len(sources)} sources, {len(raw_corpus)} characters")
        
        if not sources:
            logger.error("🚨 No sources were successfully scraped! This will cause analysis to fail.")
        
        return ResearchOutput(query=query, sources=sources, raw_corpus=raw_corpus)

    def to_dict(self, output: ResearchOutput) -> Dict[str, Any]:
        return asdict(output)

