import arxiv
from shared.schemas import ArxivPaper

class ArxivTool:
    def __init__(self):
        self.client = arxiv.Client()

    async def search(self, query: str, max_results: int = 5):
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        results = []
        for res in self.client.results(search):
            # We bundle the Title and ID together immediately
            results.append({
                "id": res.entry_id.split('/')[-1],
                "title": res.title,
                "url": res.pdf_url,
                "summary": res.summary[:200] + "..." # Snippet for the LLM to decide
            })
        return results