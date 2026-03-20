from typing import Dict, Any
from packages.core.providers.groq import GroqProvider
from packages.core.database.vector_store import VectorService

async def manager_node(state: Dict[str, Any]):
    # Use your custom provider
    provider = GroqProvider(model_name="llama-3.3-70b-versatile")
    vector_db = VectorService()
    
    query = state["messages"][-1].content
    
    # Check if we already have context in ChromaDB
    existing_docs = await vector_db.query(query, k=1)
    has_data = len(existing_docs) > 0

    prompt = f"""
    Analyze this user request: "{query}"
    Data exists in local library: {"YES" if has_data else "NO"}
    
    Task: Decide the next step.
    - Respond 'EDUCATE' if the data exists or it's a general question.
    - Respond 'RESEARCH' ONLY if we need to find/download a new paper.
    
    Respond with ONLY the word 'RESEARCH' or 'EDUCATE'.
    """
    
    response = await provider.generate(prompt, history=[])
    decision = response.content.strip().upper()

    return {
        "next_step": "researcher" if "RESEARCH" in decision else "educator"
    }