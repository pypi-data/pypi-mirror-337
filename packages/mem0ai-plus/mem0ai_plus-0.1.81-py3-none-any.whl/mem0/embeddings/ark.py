import os
from typing import Literal, Optional

from volcenginesdkarkruntime import Ark

from mem0.configs.embeddings.base import BaseEmbedderConfig
from mem0.embeddings.base import EmbeddingBase


class ArkEmbedding(EmbeddingBase):
    def __init__(self, config: Optional[BaseEmbedderConfig] = None):
        super().__init__(config)

        self.config.model = self.config.model or "doubao-embedding-text-240715"
        api_key = self.config.api_key or os.getenv("VOLCENGINE_API_KEY")
        # TODO: check if this is correct
        self.config.embedding_dims = self.config.embedding_dims or 768
        self.client = Ark(api_key=api_key)

    def embed(self, text, memory_action: Optional[Literal["add", "search", "update"]] = None):
        """
        Get the embedding for the given text using volcengine Ark.

        Args:
            text (str): The text to embed.
            memory_action (optional): The type of embedding to use. Must be one of "add", "search", or "update". Defaults to None.
        Returns:
            list: The embedding vector.
        """

        return self.client.embeddings.create(model=self.config.model, input=[text]).data[0].embedding
