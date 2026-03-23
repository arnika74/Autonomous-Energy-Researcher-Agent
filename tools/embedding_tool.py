from __future__ import annotations

from langchain_huggingface import HuggingFaceEmbeddings

from config.settings import settings


class EmbeddingTool:
    def __init__(self, model_name: str | None = None):
        self.model_name = model_name or settings.embedding_model_name
        self._embeddings = HuggingFaceEmbeddings(model_name=self.model_name)

    @property
    def embeddings(self) -> HuggingFaceEmbeddings:
        return self._embeddings
