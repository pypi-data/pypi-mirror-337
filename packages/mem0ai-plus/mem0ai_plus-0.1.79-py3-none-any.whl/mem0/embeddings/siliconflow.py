import json
import os
from typing import Literal, Optional

import requests
from mem0.configs.embeddings.base import BaseEmbedderConfig
from mem0.embeddings.base import EmbeddingBase


class SiliconFlowEmbedding(EmbeddingBase):
    def __init__(self, config: Optional[BaseEmbedderConfig] = None):
        super().__init__(config)

        self.config.model = self.config.model or "netease-youdao/bce-embedding-base_v1"
        self.api_key = self.config.api_key or os.getenv("SILICON_FLOW_API_KEY")
        # TODO: check if this is correct
        self.config.embedding_dims = self.config.embedding_dims or 768
        self.url = "https://api.siliconflow.cn/v1/embeddings"

    def embed(self, text, memory_action: Optional[Literal["add", "search", "update"]] = None):
        """
        Get the embedding for the given text using SILICON API.

        Args:
            text (str): The text to embed.
            memory_action (optional): The type of embedding to use. Must be one of "add", "search", or "update". Defaults to None.
        Returns:
            list: The embedding vector.
        """
        payload = {
            "model": self.config.model,
            "input": text,
            "encoding_format": "float"
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", self.url, json=payload, headers=headers)
        return json.loads(response.text)["data"][0]["embedding"]
