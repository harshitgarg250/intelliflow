"""
Agent database model
AI agents को represent करता है
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from enum import Enum
from app.database import Base

class AgentStatus(str, Enum):
    """Agent का status क्या है"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"

class Agent(Base):
    """
    Agent database model
    
    एक Agent एक AI assistant है जिसके पास:
    - एक role है (e.g., "Data Analyst")
    - एक goal है (क्या करना है)
    - tools हैं (क्या use कर सकता है)
    - एक LLM model है (कौन सा AI brain)
    """
    __tablename__ = "agents"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    goal = Column(String(500), nullable=False)
    backstory = Column(String(1000), nullable=False)
    llm_model = Column(String(50), default="gpt-4")
    tools = Column(JSON, default=list)  # Tools जो agent use कर सकता है
    status = Column(SQLEnum(AgentStatus), default=AgentStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="agents")
    tasks = relationship("Task", back_populates="agent")
    
    def __repr__(self):
        return f"<Agent(id={self.id}, name={self.name}, role={self.role})>"
