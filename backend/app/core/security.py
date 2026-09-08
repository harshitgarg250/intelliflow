"""
Security utilities
JWT tokens, password hashing सब यहाँ है
"""

from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

# Password को hash करने के लिए bcrypt
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# JWT configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

class SecurityUtils:
    """
    सभी security-related functions
    """
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Password को hash करना (एक-तरफा encryption)
        
        Example:
        plain_password = "MyPassword123!"
        hashed = hash_password(plain_password)
        # hashed = $2b$12$... (bcrypt format)
        
        अब plain password को देखकर हashed नहीं निकाल सकते!
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Check करना कि दिया हुआ password सही है या नहीं
        
        Example:
        is_correct = verify_password("MyPassword123!", hashed_from_db)
        # is_correct = True/False
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        JWT access token बनाना
        Frontend को यह token देंगे, frontend हर request में भेजेगा
        
        Example:
        token = create_access_token({"sub": "user_id"})
        # token = "eyJhbGc..." (JWT format)
        
        Server यह token को verify कर सकता है (no database query!)
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: dict) -> str:
        """
        Refresh token बनाना
        Access token expire हो जाए तो यह से नया access token बना सकते हैं
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> dict:
        """
        Token को verify करना
        सही है या expired?
        
        Returns:
        - अगर valid: data dict
        - अगर invalid: None
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError as e:
            logger.error(f"Token verification failed: {e}")
            return None
