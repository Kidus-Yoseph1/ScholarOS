"""
packages/core/providers/base.py
Defines the Abstract Base Class for all LLM providers.
Rule #2 & #5: Ensures consistent interface for multi-provider fallback.
"""

from abc import ABC, abstractmethod
from typing import AsyncGenerator, List, Dict, Any
from shared.schemas import ChatResponse

class BaseProvider(ABC):
    """
    Abstract Base Class (Contract).
    All LLM integrations must implement these methods.
    """

    @abstractmethod
    async def generate(
        self, 
        prompt: str, 
        history: List[Dict[str, str]], 
        **kwargs
    ) -> ChatResponse:
        """Non-streaming response for logic-heavy tasks (e.g., Quiz generation)."""
        pass

    @abstractmethod
    async def stream(
        self, 
        prompt: str, 
        history: List[Dict[str, str]], 
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Streaming response for React frontend UX."""
        pass