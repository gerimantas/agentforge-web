"""
Configuration management for AgentForge-Web

Handles environment variables and application settings.
"""

from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Configuration
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "AgentForge Web"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "sqlite:///./agentforge.db"  # Default for development
    
    # Security
    SECRET_KEY: str = "change-this-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # AgentForge Configuration
    OPENAI_API_KEY: Optional[str] = None
    SERPER_API_KEY: Optional[str] = None
    MAX_AGENT_ITERATIONS: int = 3
    AGENT_TIMEOUT: int = 300  # 5 minutes in seconds
    
    # Development
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()
