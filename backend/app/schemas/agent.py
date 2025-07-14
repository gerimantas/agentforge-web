"""
Agent schemas for API validation

Pydantic models for agent-related API requests and responses.
"""

from pydantic import BaseModel
from typing import Optional, List, Any, Literal
from datetime import datetime

class AgentRequest(BaseModel):
    """Schema for agent execution request"""
    query: str
    workflow_type: Literal["execution", "maintenance"] = "execution"

class AgentUpdate(BaseModel):
    """Schema for real-time agent updates"""
    type: Literal["status", "result", "error"]
    status: str
    message: str
    current_agent: Optional[str] = None
    progress: Optional[int] = None
    result: Optional[str] = None
    error: Optional[str] = None
    timestamp: datetime = datetime.utcnow()

class AgentSessionBase(BaseModel):
    """Base agent session schema"""
    query: str
    workflow_type: str = "execution"

class AgentSessionCreate(AgentSessionBase):
    """Schema for creating agent session"""
    pass

class AgentSessionUpdate(BaseModel):
    """Schema for updating agent session"""
    status: Optional[str] = None
    current_agent: Optional[str] = None
    progress: Optional[int] = None
    intermediate_results: Optional[List[Any]] = None
    final_result: Optional[str] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class AgentSessionResponse(AgentSessionBase):
    """Schema for agent session response"""
    id: int
    user_id: int
    status: str
    current_agent: Optional[str] = None
    progress: int
    intermediate_results: List[Any]
    final_result: Optional[str] = None
    error_message: Optional[str] = None
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AgentResponse(BaseModel):
    """Schema for agent execution response"""
    session_id: int
    status: str
    message: str
