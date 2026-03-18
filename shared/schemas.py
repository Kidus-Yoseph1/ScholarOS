"""
shared/schemas.py
Standardized Data Contracts for Scholar-OS.
Ensures type safety between FastAPI, LangGraph, and multiple LLM providers.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl

# Provider & Model Enumerations

class ProviderName(str, Enum):
    GEMINI = "gemini"
    GROQ = "groq"
    OLLAMA = "ollama"

class ModelTier(str, Enum):
    """Categorizes models for the Router Agent to choose the right tool for the job."""
    SOTA = "sota"        # Gemini Pro / GPT-4 level
    FAST = "fast"        # Groq / Gemini Flash level
    LOCAL = "local"      # Ollama / Llama 3 level

# Knowledge Base Schemas 

class ArxivPaper(BaseModel):
    """Schema for research papers fetched from ArXiv."""
    paper_id: str
    title: str
    authors: List[str]
    summary: str
    pdf_url: HttpUrl
    published_date: str
    content: Optional[str] = None  # Raw text extracted for Vector DB

class SourceChunk(BaseModel):
    """A specific snippet retrieved from the Vector DB for RAG."""
    text: str
    source_id: str
    page_number: Optional[int] = None
    similarity_score: float

# LangGraph State Schema 

class AgentState(BaseModel):
    """
    The 'Source of Truth' passed between LangGraph nodes.
    Represents the current status of the agentic workflow.
    """
    query: str = Field(..., description="The user's original input request.")
    history: List[Dict[str, str]] = Field(default_factory=list)
    current_agent: str = "manager"
    
    # Context & Tools
    documents: List[ArxivPaper] = Field(default_factory=list)
    retrieved_chunks: List[SourceChunk] = Field(default_factory=list)
    
    # Outputs
    notes_markdown: str = ""
    generated_quizzes: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Error Handling (Rule #1: Failure Isolation)
    error: Optional[str] = None
    next_step: Optional[str] = None

# API Response Schemas 

class ChatResponse(BaseModel):
    """Standardized response for the React Frontend."""
    agent_id: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    error: bool = False

class ProviderConfig(BaseModel):
    """Configuration for dynamic provider switching (Rule #5)."""
    provider: ProviderName
    model_name: str
    temperature: float = 0.1
    max_tokens: int = 4096