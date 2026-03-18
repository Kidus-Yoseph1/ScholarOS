import os
from typing import AsyncGenerator, List, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from packages.core.providers.base import BaseProvider
from shared.schemas import ChatResponse
from dotenv import load_dotenv

load_dotenv()

class GeminiProvider(BaseProvider):
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name
        self.model = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.1
        )

    async def generate(self, prompt: str, history: List[Dict[str, str]], **kwargs) -> ChatResponse:
        try:
            response = await self.model.ainvoke(prompt)
            return ChatResponse(
                agent_id="gemini",
                content=str(response.content),
                metadata={"model": self.model.model}
            )
        except Exception as e:
            return ChatResponse(agent_id="gemini", content="", error=True, metadata={"detail": str(e)})

    async def stream(self, prompt: str, history: List[Dict[str, str]], **kwargs) -> AsyncGenerator[str, None]:
        async for chunk in self.model.astream(prompt):
            yield str(chunk.content)