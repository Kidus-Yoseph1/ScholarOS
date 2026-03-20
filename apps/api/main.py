from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from packages.core.graph.builder import scholar_os
from langchain_core.messages import HumanMessage

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        inputs = {"messages": [HumanMessage(content=request.message)]}
        final_state = await scholar_os.ainvoke(inputs)
        
        last_msg = final_state["messages"][-1]
        content = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)
        
        return {
            "response": content,
            "title": final_state.get("current_paper_title", "General Research")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))