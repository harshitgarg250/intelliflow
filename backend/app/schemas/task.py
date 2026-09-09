from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=10)
    expected_output: Optional[str] = None
    agent_id: Optional[str] = None
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    expected_output: Optional[str] = None
    agent_id: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None

class TaskResponse(BaseModel):
    id: str
    user_id: str
    agent_id: Optional[str]
    title: str
    description: str
    expected_output: Optional[str]
    priority: TaskPriority
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True