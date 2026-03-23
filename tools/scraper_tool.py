from __future__ import annotations

import re
import time
from dataclasses import dataclass
from typing import Optional

import requests
from bs4 import BeautifulSoup

from config.settings import settings


@dataclass
class ScrapedPage:
    url: str
    title: str | None
    text: str


def _clean_text(text: str) -> str:
    # Normalize whitespace, remove boilerplate-y repeated spaces.
    text = re.sub(r"\s+", " ", text)
    return text.strip()


class WebScraperTool:
    """
    Scraper that tries Selenium first (dynamic sites), falls back to requests+BS4.
    Selenium requires a working WebDriver (chromedriver/geckodriver) on PATH.
    """

    def __init__(self, headless: Optional[bool] = None):
        self.headless = settings.selenium_headless if headless is None else headless

    def scrape(self, url: str) -> ScrapedPage:
        # Skip Selenium entirely - use requests only for reliability
        # Selenium requires Chrome WebDriver which may not be installed
        return self._scrape_with_requests(url)

    def _scrape_with_requests(self, url: str) -> ScrapedPage:
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"🌐 Scraping with requests: {url}")
        
        r = requests.get(
            url,
            timeout=settings.request_timeout_s,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            },
        )
        r.raise_for_status()
        logger.info(f"✅ HTTP {r.status_code} for {url}")
        
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
            tag.decompose()
        title = soup.title.get_text(strip=True) if soup.title else None
        text = soup.get_text(" ", strip=True)
        text = _clean_text(text)[: settings.max_chars_per_page]
        
        logger.info(f"📄 Extracted {len(text)} chars, title: {title}")
        return ScrapedPage(url=url, title=title, text=text)

    def _scrape_with_selenium(self, url: str) -> ScrapedPage:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        options = Options()
        if self.headless:
            # New headless mode for recent Chrome.
            options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,800")

        driver = webdriver.Chrome(options=options)
        try:
            driver.set_page_load_timeout(settings.selenium_page_load_timeout_s)
            driver.get(url)
            time.sleep(2.0)  # allow some client-side rendering
            html = driver.page_source
        finally:
            driver.quit()

        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
            tag.decompose()
        title = soup.title.get_text(strip=True) if soup.title else None
        text = soup.get_text(" ", strip=True)
        text = _clean_text(text)[: settings.max_chars_per_page]
        return ScrapedPage(url=url, title=title, text=text)
