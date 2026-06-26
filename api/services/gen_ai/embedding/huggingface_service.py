"""Hugging Face embedding service.

Embeds text and performs vector similarity search via the local database.
"""

from typing import Any, Dict, List, Optional

import httpx
from loguru import logger

from api.db.db_client import DBClient
from api.utils.url_security import validate_user_configured_service_url

from .base import BaseEmbeddingService

DEFAULT_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_BASE_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/"
DB_EMBEDDING_DIMENSION = 1536  # The database requires 1536 dimensions


class HuggingFaceAPIKeyNotConfiguredError(Exception):
    """Raised when Hugging Face API key is not configured for embeddings."""

    def __init__(self):
        super().__init__(
            "Hugging Face API key not configured. Please set your API key in "
            "Model Configurations > Embedding to use document processing."
        )


class HuggingFaceEmbeddingService(BaseEmbeddingService):
    """Embedding service using Hugging Face Inference API."""

    def __init__(
        self,
        db_client: DBClient,
        api_key: Optional[str] = None,
        model_id: str = DEFAULT_MODEL_ID,
        base_url: Optional[str] = None,
    ):
        """Initialize the Hugging Face embedding service.

        Args:
            db_client: Database client for vector similarity search.
            api_key: Hugging Face API key.
            model_id: Hugging Face model identifier.
            base_url: Base URL for the Inference API.
        """
        self.db = db_client
        self.model_id = model_id
        
        # Format the URL properly if standard HF inference URL is used
        if not base_url or base_url == DEFAULT_BASE_URL:
            self.base_url = f"{DEFAULT_BASE_URL.rstrip('/')}/{model_id}"
        else:
            self.base_url = base_url
            validate_user_configured_service_url(
                self.base_url,
                field_name="base_url",
            )

        self.api_key = api_key
        self._api_key_configured = bool(api_key)
        if self._api_key_configured:
            logger.info(f"Hugging Face embedding service initialized with model: {model_id}")
        else:
            logger.warning(
                "Hugging Face embedding service initialized without API key. "
                "Operations will fail until API key is configured in Model Configurations."
            )

    def get_model_id(self) -> str:
        """Return the model identifier."""
        return self.model_id

    def get_embedding_dimension(self) -> int:
        """Return the embedding dimension.
        We return 1536 because we pad vectors to match the database schema.
        """
        return DB_EMBEDDING_DIMENSION

    def _ensure_api_key_configured(self):
        """Check if API key is configured and raise error if not."""
        if not self._api_key_configured:
            raise HuggingFaceAPIKeyNotConfiguredError()

    def _pad_vector(self, vector: List[float], target_dim: int = DB_EMBEDDING_DIMENSION) -> List[float]:
        """Pad a vector with zeros to match the target dimension.
        
        This is required because pgvector is strictly configured to 1536 dimensions
        in the knowledge_base_chunks table schema.
        Zero-padding preserves cosine similarity perfectly because adding zeros
        does not change the dot product or the vector magnitude.
        """
        if len(vector) >= target_dim:
            return vector[:target_dim]
        return vector + [0.0] * (target_dim - len(vector))

    async def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Embed a batch of texts using Hugging Face API.

        Raises:
            HuggingFaceAPIKeyNotConfiguredError: If API key is not configured.
        """
        self._ensure_api_key_configured()

        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json={"inputs": texts, "options": {"wait_for_model": True}},
                    timeout=30.0
                )
                response.raise_for_status()
                embeddings = response.json()
                
                padded_embeddings = [self._pad_vector(emb) for emb in embeddings]
                return padded_embeddings
        except Exception as e:
            logger.error(f"Error generating Hugging Face embeddings: {e}")
            raise

    async def embed_query(self, query: str) -> List[float]:
        """Embed a single query text using Hugging Face API.

        Raises:
            HuggingFaceAPIKeyNotConfiguredError: If API key is not configured.
        """
        self._ensure_api_key_configured()
        embeddings = await self.embed_texts([query])
        return embeddings[0]

    async def search_similar_chunks(
        self,
        query: str,
        organization_id: int,
        limit: int = 5,
        document_uuids: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Search for similar chunks using vector similarity.

        Raises:
            HuggingFaceAPIKeyNotConfiguredError: If API key is not configured.
        """
        self._ensure_api_key_configured()

        query_embedding = await self.embed_query(query)

        return await self.db.search_similar_chunks(
            query_embedding=query_embedding,
            organization_id=organization_id,
            limit=limit,
            document_uuids=document_uuids,
            embedding_model=self.model_id,
        )
