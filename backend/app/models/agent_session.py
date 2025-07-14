"""
Agent Session database model

Defines the AgentSession table for tracking agent execution history.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .user import Base

class AgentSession(Base):
    """Agent execution session model"""
    __tablename__ = "agent_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Session details
    query = Column(Text, nullable=False)
    workflow_type = Column(String(20), default="execution")  # execution or maintenance
    status = Column(String(20), default="queued")  # queued, analyzing, executing, completed, failed
    
    # Execution tracking
    current_agent = Column(String(100))
    progress = Column(Integer, default=0)
    intermediate_results = Column(JSON, default=list)
    final_result = Column(Text)
    error_message = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    
    def __repr__(self):
        return f"<AgentSession(id={self.id}, user_id={self.user_id}, status='{self.status}')>"
