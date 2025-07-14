"""
Dependency injection for FastAPI endpoints

Provides common dependencies like database sessions and user authentication.
"""

from fastapi import Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional

from ..core.security import verify_token
from ..models import User
from ..database import get_database

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_db() -> Session:
    """Get database session dependency"""
    return next(get_database())


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token"""
    
    # For development/testing - create a mock user if no token validation
    # TODO: Replace with actual token validation
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Mock user for development - replace with actual token verification
    mock_user = User(
        id=1,
        email="test@example.com", 
        hashed_password="hashed",
        is_active=True
    )
    
    return mock_user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user (ensure user is not disabled)"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


async def get_current_user_from_query(
    token: Optional[str] = Query(None),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from query parameter token (for SSE)"""
    
    # For development/testing - create a mock user
    # TODO: Replace with actual token validation
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated - token required in query parameter",
        )
    
    # Mock user for development - replace with actual token verification
    mock_user = User(
        id=1,
        email="test@example.com", 
        hashed_password="hashed",
        is_active=True
    )
    
    return mock_user
