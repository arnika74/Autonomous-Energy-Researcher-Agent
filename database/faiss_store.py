from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from langchain_community.docstore.document import Document
from langchain_community.vectorstores import FAISS

from config.settings import settings
from tools.embedding_tool import EmbeddingTool


class FaissKnowledgeBase:
    """
    Persists a FAISS index locally and supports similarity search over past reports.
    """

    def __init__(self, faiss_dir: Optional[Path] = None, embedding_tool: Optional[EmbeddingTool] = None):
        self.faiss_dir = faiss_dir or settings.faiss_dir
        self.faiss_dir.mkdir(parents=True, exist_ok=True)
        self.embedding_tool = embedding_tool or EmbeddingTool()
        self._vs: Optional[FAISS] = None

    def _index_path(self) -> Path:
        return self.faiss_dir / "index"

    def load(self) -> None:
        index_path = self._index_path()
        if index_path.exists():
            self._vs = FAISS.load_local(
                folder_path=str(index_path),
                embeddings=self.embedding_tool.embeddings,
                allow_dangerous_deserialization=True,
            )

    def _ensure_loaded(self) -> None:
        if self._vs is None:
            self.load()

    def add_report(self, report_id: str, query: str, report_text: str) -> None:
        self._ensure_loaded()
        doc = Document(page_content=report_text, metadata={"report_id": report_id, "query": query})
        if self._vs is None:
            self._vs = FAISS.from_documents([doc], self.embedding_tool.embeddings)
        else:
            self._vs.add_documents([doc])
        self.save()

    def save(self) -> None:
        if self._vs is None:
            return
        self._vs.save_local(str(self._index_path()))

    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        self._ensure_loaded()
        if self._vs is None:
            return []
        return self._vs.similarity_search(query, k=k)

