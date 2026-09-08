"""
User database model
Database में exactly कैसा table होगा, यहाँ define करते हैं
"""

from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database import Base

class User(Base):
    """
    User/Account model
    
    Database में यह एक table होगी:
    users table
    ├── id (unique identifier)
    ├── username (login के लिए)
    ├── email (email)
    ├── password_hash (encrypted password)
    ├── is_active (user active है या नहीं)
    ├── created_at (कब create हुआ)
    └── updated_at (कब update हुआ)
    """
    __tablename__ = "users"
    
    # Columns define करें
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - एक user के पास multiple agents हो सकते हैं
    agents = relationship("Agent", back_populates="user", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    workflows = relationship("Workflow", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
