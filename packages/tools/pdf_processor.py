import fitz  
import httpx
import io
from typing import List

class PDFProcessor:
    async def download_and_extract(self, url: str) -> str:
        """Downloads PDF and extracts raw text."""
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                return ""
            
            doc = fitz.open(stream=io.BytesIO(response.content), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text("text") + "\n"
            return text

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 150) -> List[str]:
        """Splits text into chunks so the LLM can handle the context."""
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunks.append(text[i : i + chunk_size])
        return chunks