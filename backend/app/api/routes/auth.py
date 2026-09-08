"""
Authentication endpoints
Register और Login
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.models.user import User
from app.database import get_db
from app.core.security import SecurityUtils
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    नया user register करना
    
    Request:
    {
        "username": "harshit",
        "email": "harshit@example.com",
        "password": "SecurePass123!"
    }
    
    Response:
    {
        "access_token": "eyJhbGc...",
        "refresh_token": "eyJhbGc...",
        "token_type": "bearer",
        "user": {...}
    }
    """
    try:
        # Check if user already exists
        stmt = select(User).where(User.email == user_data.email)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if username exists
        stmt = select(User).where(User.username == user_data.username)
        result = await db.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Create new user
        hashed_password = SecurityUtils.hash_password(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        logger.info(f"New user registered: {new_user.email}")
        
        # Create tokens
        access_token = SecurityUtils.create_access_token(
            data={"sub": str(new_user.id), "email": new_user.email}
        )
        refresh_token = SecurityUtils.create_refresh_token(
            data={"sub": str(new_user.id), "email": new_user.email}
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse.from_orm(new_user)
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Registration error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    User login करना
    
    Request:
    {
        "email": "harshit@example.com",
        "password": "SecurePass123!"
    }
    """
    try:
        # Find user by email
        stmt = select(User).where(User.email == credentials.email)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not SecurityUtils.verify_password(credentials.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        logger.info(f"User logged in: {user.email}")
        
        # Create tokens
        access_token = SecurityUtils.create_access_token(
            data={"sub": str(user.id), "email": user.email}
        )
        refresh_token = SecurityUtils.create_refresh_token(
            data={"sub": str(user.id), "email": user.email}
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse.from_orm(user)
        )
    
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )
