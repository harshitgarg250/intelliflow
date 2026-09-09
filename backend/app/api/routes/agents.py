import logging
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.agent import Agent
from app.schemas.agent import AgentCreate, AgentResponse, AgentUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agents", tags=["Agents"])


async def get_current_user_id(db: AsyncSession = Depends(get_db)) -> str:
    return "00000000-0000-0000-0000-000000000001"


@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    try:
        agent = Agent(
            id=uuid.uuid4(),
            user_id=uuid.UUID(user_id),
            name=agent_data.name,
            role=agent_data.role,
            goal=agent_data.goal,
            backstory=agent_data.backstory,
            llm_model=agent_data.llm_model,
            tools=agent_data.tools,
        )
        db.add(agent)
        await db.commit()
        await db.refresh(agent)
        return agent
    except Exception as exc:
        await db.rollback()
        logger.exception("Error creating agent: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to create agent") from exc


@router.get("", response_model=List[AgentResponse])
async def list_agents(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Agent).where(Agent.user_id == uuid.UUID(user_id)))
    return result.scalars().all()


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Agent).where(
            Agent.id == uuid.UUID(agent_id),
            Agent.user_id == uuid.UUID(user_id),
        )
    )
    agent = result.scalar_one_or_none()
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent_data: AgentUpdate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    agent = await get_agent(agent_id, user_id, db)
    for field, value in agent_data.model_dump(exclude_unset=True).items():
        setattr(agent, field, value)
    await db.commit()
    await db.refresh(agent)
    return agent


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    agent = await get_agent(agent_id, user_id, db)
    await db.delete(agent)
    await db.commit()
