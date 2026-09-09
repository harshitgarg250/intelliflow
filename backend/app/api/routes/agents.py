from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.agent import AgentCreate, AgentUpdate, AgentResponse
from app.models.agent import Agent
from app.database import get_db
from typing import List
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agents", tags=["Agents"])

async def get_current_user_id(db: AsyncSession = Depends(get_db)):
    """Demo: सब के लिए fixed user ID"""
    return "00000000-0000-0000-0000-000000000001"

@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """नया agent बनाएं"""
    try:
        new_agent = Agent(
            id=uuid.uuid4(),
            user_id=uuid.UUID(user_id),
            name=agent_data.name,
            role=agent_data.role,
            goal=agent_data.goal,
            backstory=agent_data.backstory,
            llm_model=agent_data.llm_model,
            tools=agent_data.tools
        )
        
        db.add(new_agent)
        await db.commit()
        await db.refresh(new_agent)
        
        logger.info(f"Agent created: {new_agent.id}")
        return new_agent
    
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create agent"
        )

@router.get("", response_model=List[AgentResponse])
async def list_agents(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """सभी agents को list करें"""
    try:
        stmt = select(Agent).where(Agent.user_id == uuid.UUID(user_id))
        result = await db.execute(stmt)
        agents = result.scalars().all()
        return agents
    
    except Exception as e:
        logger.error(f"Error listing agents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch agents"
        )

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """एक agent की details"""
    try:
        stmt = select(Agent).where(
            (Agent.id == uuid.UUID(agent_id)) &
            (Agent.user_id == uuid.UUID(user_id))
        )
        result = await db.execute(stmt)
        agent = result.scalar_one_or_none()
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )
        
        return agent
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch agent"
        )

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent_data: AgentUpdate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Agent को update करें"""
    try:
        stmt = select(Agent).where(
            (Agent.id == uuid.UUID(agent_id)) &
            (Agent.user_id == uuid.UUID(user_id))
        )
        result = await db.execute(stmt)
        agent = result.scalar_one_or_none()
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )
        
        # Update only provided fields
        update_data = agent_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(agent, field, value)
        
        await db.commit()
        await db.refresh(agent)
        
        logger.info(f"Agent updated: {agent_id}")
        return agent
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating agent: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update agent"
        )

@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Agent को delete करें"""
    try:
        stmt = select(Agent).where(
            (Agent.id == uuid.UUID(agent_id)) &
            (Agent.user_id == uuid.UUID(user_id))
        )
        result = await db.execute(stmt)
        agent = result.scalar_one_or_none()
        
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )
        
        await db.delete(agent)
        await db.commit()
        
        logger.info(f"Agent deleted: {agent_id}")
        return None
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting agent: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete agent"
        )