from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from shared.schemas import SourceChunk
from typing import List

class VectorService:
    def __init__(self, collection_name: str = "scholar_docs"):
        # Local-first, lightweight embedding model
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}, 
            encode_kwargs={'normalize_embeddings': True}
        )
        
        self.persist_dir = "./.vector_db"
        
        self.vector_store = Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_dir
        )

    async def upsert_papers(self, chunks: List[str], paper_id: str, title: str):
        """
        Saves chunks and ensures EVERY chunk knows its parent paper's title and ID.
        """
        metadatas = [
            {
                "paper_id": paper_id,
                "title": title,
                "chunk_index": i
            } for i in range(len(chunks))
        ]
        
        try:
            self.vector_store.add_texts(texts=chunks, metadatas=metadatas)
            return True
        except Exception as e:
            print(f"Vector Store Error: {e}")
            return False

    async def query(self, question: str, k: int = 4) -> List[SourceChunk]:
        """Similarity search to find the most relevant paper snippets."""
        try:
            # We use similarity_search_with_score to get the 'distance'
            docs_and_scores = self.vector_store.similarity_search_with_score(question, k=k)
            
            results = []
            for doc, score in docs_and_scores:
                results.append(SourceChunk(
                    text=doc.page_content,
                    source_id=doc.metadata.get("paper_id", "unknown"),
                    page_number=doc.metadata.get("page", 0),
                    similarity_score=float(score), 
                    metadata={
                        "title": doc.metadata.get("title", "Unknown Paper"),
                        "chunk": doc.metadata.get("chunk_index", 0)
                    }
                ))
            return results
        except Exception as e:
            print(f"Query Error: {e}")
            return []