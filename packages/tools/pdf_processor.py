import fitz  
import httpx
import io
from typing import List

class PDFProcessor:
    async def download_and_extract(self, url: str) -> str:
        """Downloads PDF to memory and extracts raw text."""
        async with httpx.AsyncClient(timeout=60.0) as client:
            print(f"📡 Downloading PDF: {url}")
            response = await client.get(url)
            
            if response.status_code != 200:
                print(f" Failed to download: {response.status_code}")
                return ""
            
            # This opens the PDF from the raw bytes in RAM (no file saved to disk)
            doc = fitz.open(stream=io.BytesIO(response.content), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text("text") + "\n"
            
            print(f"✅ Extracted {len(text)} characters from memory.")
            return text

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 150) -> List[str]:
        """Splits text into chunks for the Vector DB."""
        chunks = []
        # Basic sliding window chunking
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i : i + chunk_size]
            if chunk:
                chunks.append(chunk)
        return chunks