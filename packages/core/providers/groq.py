import os
from dotenv import load_dotenv
from typing import AsyncGenerator, List, Dict
from langchain_groq import ChatGroq
from packages.core.providers.base import BaseProvider
from shared.schemas import ChatResponse

load_dotenv()

class GroqProvider(BaseProvider):
    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        self.model_name = model_name 
        api_key = os.getenv("GROQ_API_KEY")
        
        if not api_key:
            raise ValueError("GROQ_API_KEY is missing from .env")

        self.model = ChatGroq(
            model_name=self.model_name,
            groq_api_key=api_key,
            temperature=0.1
        )

    async def generate(self, prompt: str, history: List[Dict[str, str]], **kwargs) -> ChatResponse:
        try:
            response = await self.model.ainvoke(prompt)
            return ChatResponse(
                agent_id="groq",
                content=str(response.content),
                metadata={"model": self.model_name}
            )
        except Exception as e:
            print(f"DEBUG: Groq API Error -> {e}") 
            return ChatResponse(
                agent_id="groq", 
                content="API Error occurred.", 
                error=True, 
                metadata={"detail": str(e), "model": self.model_name}
            )

    async def stream(self, prompt: str, history: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        async for chunk in self.model.astream(prompt):
            yield str(chunk.content)