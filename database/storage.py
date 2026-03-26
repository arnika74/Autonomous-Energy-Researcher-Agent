from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from config.settings import settings


@dataclass
class ReportRecord:
    id: str
    query: str
    title: str
    introduction: str
    key_findings: List[str]
    conclusion: str
    sources: List[Dict[str, Any]]
    created_at: str


def _slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:80] or "report"


class LocalStorage:
    def __init__(self, reports_dir: Optional[Path] = None):
        self.reports_dir = reports_dir or settings.reports_dir
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def save_report(self, record: ReportRecord) -> Path:
        base = f"{record.created_at}_{_slugify(record.query)}_{record.id}"
        path_json = self.reports_dir / f"{base}.json"
        path_txt = self.reports_dir / f"{base}.txt"

        path_json.write_text(json.dumps(asdict(record), indent=2, ensure_ascii=False), encoding="utf-8")

        txt = self._format_text(record)
        path_txt.write_text(txt, encoding="utf-8")
        return path_json

    def list_reports(self, limit: int = 20) -> List[ReportRecord]:
        files = sorted(self.reports_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
        out: List[ReportRecord] = []
        for p in files[:limit]:
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                out.append(ReportRecord(**data))
            except Exception:
                continue
        return out

    def _format_text(self, record: ReportRecord) -> str:
        parts = [
            f"Title: {record.title}",
            "",
            "Introduction",
            record.introduction,
            "",
            "Key Findings",
        ]
        for i, k in enumerate(record.key_findings, 1):
            parts.append(f"{i}. {k}")
        parts += [
            "",
            "Conclusion",
            record.conclusion,
            "",
            "Sources",
        ]
        for s in record.sources:
            parts.append(f"- {s.get('title') or ''} ({s.get('url')})")
        parts.append("")
        return "\n".join(parts)


def new_report_id() -> str:
    # short deterministic-ish ID without external deps
    now = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    return now[-10:]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
