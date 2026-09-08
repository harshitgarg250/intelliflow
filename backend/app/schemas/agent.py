"""
Agent Pydantic schemas
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class AgentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"

class AgentCreate(BaseModel):
    """नया agent बनाते समय"""
    name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., min_length=1, max_length=100)
    goal: str = Field(..., min_length=10, max_length=500)
    backstory: str = Field(..., min_length=10, max_length=1000)
    llm_model: str = Field(default="gpt-4", max_length=50)
    tools: List[str] = Field(default=[], description="Tool names")
    
    class Config:
        example = {
            "name": "Data Analyst",
            "role": "Senior Data Analyst",
            "goal": "Analyze data and provide insights",
            "backstory": "10 years of data science experience",
            "llm_model": "gpt-4",
            "tools": ["python", "sql", "pandas"]
        }

class AgentUpdate(BaseModel):
    """Agent update करते समय - सभी optional"""
    name: Optional[str] = None
    role: Optional[str] = None
    goal: Optional[str] = None
    backstory: Optional[str] = None
    llm_model: Optional[str] = None
    tools: Optional[List[str]] = None
    status: Optional[AgentStatus] = None

class AgentResponse(BaseModel):
    """Agent information return करते समय"""
    id: str
    user_id: str
    name: str
    role: str
    goal: str
    backstory: str
    llm_model: str
    tools: List[str]
    status: AgentStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
