from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import List

from ddgs import DDGS  # Updated from duckduckgo_search to ddgs

from config.settings import settings

logger = logging.getLogger(__name__)


@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str | None = None


class DuckDuckGoSearchTool:
    def __init__(self, max_results: int | None = None):
        self.max_results = max_results or settings.max_search_results

    def search(self, query: str) -> List[SearchResult]:
        logger.info(f"🔍 Searching DuckDuckGo for: {query}")
        results: List[SearchResult] = []
        try:
            with DDGS() as ddgs:
                search_results = list(ddgs.text(query, max_results=self.max_results))
                logger.info(f"📊 Raw search returned {len(search_results)} results")
                
                for r in search_results:
                    url = (r.get("href") or r.get("url") or "").strip()
                    title = (r.get("title") or "").strip()
                    snippet = (r.get("body") or r.get("snippet") or "").strip() or None
                    
                    if not url:
                        continue
                    
                    results.append(SearchResult(title=title or url, url=url, snippet=snippet))
                    logger.debug(f"✅ Added result: {title[:50]}... -> {url[:50]}...")
        except Exception as e:
            logger.error(f"❌ Search failed: {str(e)}")
            return []
        
        # Deduplicate by URL while preserving order.
        seen = set()
        uniq: List[SearchResult] = []
        for r in results:
            if r.url in seen:
                continue
            seen.add(r.url)
            uniq.append(r)
        
        logger.info(f"🎯 Final search results: {len(uniq)} unique URLs")
        return uniq
