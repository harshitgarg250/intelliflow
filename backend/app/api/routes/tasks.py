from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.models.task import Task
from app.database import get_db
from typing import List
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tasks", tags=["Tasks"])

async def get_current_user_id(db: AsyncSession = Depends(get_db)):
    """Demo: fixed user ID"""
    return "00000000-0000-0000-0000-000000000001"

@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """नया task बनाएं"""
    try:
        new_task = Task(
            id=uuid.uuid4(),
            user_id=uuid.UUID(user_id),
            agent_id=uuid.UUID(task_data.agent_id) if task_data.agent_id else None,
            title=task_data.title,
            description=task_data.description,
            expected_output=task_data.expected_output,
            priority=task_data.priority
        )
        
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)
        
        logger.info(f"Task created: {new_task.id}")
        return new_task
    
    except Exception as e:
        logger.error(f"Error creating task: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task"
        )

@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """सभी tasks"""
    try:
        stmt = select(Task).where(Task.user_id == uuid.UUID(user_id))
        result = await db.execute(stmt)
        tasks = result.scalars().all()
        return tasks
    
    except Exception as e:
        logger.error(f"Error listing tasks: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch tasks"
        )

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Task details"""
    try:
        stmt = select(Task).where(
            (Task.id == uuid.UUID(task_id)) &
            (Task.user_id == uuid.UUID(user_id))
        )
        result = await db.execute(stmt)
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        return task
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching task: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch task"
        )

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Task update"""
    try:
        stmt = select(Task).where(
            (Task.id == uuid.UUID(task_id)) &
            (Task.user_id == uuid.UUID(user_id))
        )
        result = await db.execute(stmt)
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        update_data = task_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "agent_id" and value:
                setattr(task, field, uuid.UUID(value))
            else:
                setattr(task, field, value)
        
        await db.commit()
        await db.refresh(task)
        
        logger.info(f"Task updated: {task_id}")
        return task
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating task: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task"
        )

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Task delete"""
    try:
        stmt = select(Task).where(
            (Task.id == uuid.UUID(task_id)) &
            (Task.user_id == uuid.UUID(user_id))
        )
        result = await db.execute(stmt)
        task = result.scalar_one_or_none()
        
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        await db.delete(task)
        await db.commit()
        
        logger.info(f"Task deleted: {task_id}")
        return None
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting task: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task"
        )