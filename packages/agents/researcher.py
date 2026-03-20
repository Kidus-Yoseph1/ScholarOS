from packages.tools.arxiv_loader import ArxivTool
from packages.tools.pdf_processor import PDFProcessor
from packages.core.database.vector_store import VectorService
from packages.core.graph.state import AgentState

async def researcher_node(state: AgentState):
    user_query = state["messages"][-1].content
    
    arxiv = ArxivTool()
    pdf_tool = PDFProcessor()
    vector_db = VectorService()

    # Search (Librarian)
    papers = await arxiv.search(user_query, max_results=1)
    if not papers:
        return {"messages": [("assistant", "Search yielded no results.")]}
    
    paper = papers[0]
    
    # Extract & Embed (Scanner & Memory)
    text = await pdf_tool.download_and_extract(paper['url'])
    chunks = pdf_tool.chunk_text(text)
    
    await vector_db.upsert_papers(chunks, paper['id'], paper['title'])
    
    return {
        "messages": [("assistant", f"I've added '{paper['title']}' to your library.")],
        "current_paper_id": paper['id'],
        "current_paper_title": paper['title']
    }