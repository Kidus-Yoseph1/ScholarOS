from packages.core.graph.state import AgentState
from packages.core.database.vector_store import VectorService
from packages.core.providers.groq import GroqProvider

async def educator_node(state: AgentState):
    vector_db = VectorService()
    # Initialize using your internal provider package
    provider = GroqProvider(model_name="llama-3.3-70b-versatile")
    
    query = state["messages"][-1].content
    
    # Get Grounded Context
    context_chunks = await vector_db.query(query, k=5)
    context_text = "\n\n".join([c.text for c in context_chunks])
    
    prompt = f"""
    You are an AI Research Professor. 
    User Question: {query}
    
    Research Context from Library:
    {context_text}
    
    Instructions:
    1. Use the provided context for specific details.
    2. Use your internal knowledge of Machine Learning for broader concepts.
    3. Keep the tone technical and clear.
    """
    
    # Calling your custom generate method
    response = await provider.generate(prompt, history=[])
    
    return {"messages": [("assistant", response.content)]}