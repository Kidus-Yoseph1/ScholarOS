import os
from typing import AsyncGenerator, List, Dict
from langchain_ollama import ChatOllama
from packages.core.providers.base import BaseProvider
from shared.schemas import ChatResponse

class OllamaProvider(BaseProvider):
    def __init__(self, model_name: str = "llama3.2:3b"):
        self.model_name = model_name
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = ChatOllama(
            model=self.model_name,
            base_url=base_url,
            temperature=0.1
        )

    async def generate(self, prompt: str, history: List[Dict[str, str]], **kwargs) -> ChatResponse:
        try:
            response = await self.model.ainvoke(prompt)
            return ChatResponse(
                agent_id="ollama",
                content=str(response.content),
                metadata={"model": self.model_name} 
            )
        except Exception as e:
            return ChatResponse(
                agent_id="ollama", 
                content="Local model unavailable.", 
                error=True, 
                metadata={"detail": str(e)}
            )

    async def stream(self, prompt: str, history: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        async for chunk in self.model.astream(prompt):
            yield str(chunk.content)