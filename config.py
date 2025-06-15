"""
Configuration module for LINE BOT × OneDrive AI System
"""
import os
import logging
from pathlib import Path
from typing import Optional

# Try to load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Continue without dotenv if not available
    pass

class Config:
    """Application configuration class"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent
    LOGS_DIR = BASE_DIR / "logs"
    MODULES_DIR = BASE_DIR / "modules"
    
    # Ensure directories exist
    LOGS_DIR.mkdir(exist_ok=True)
    
    # LINE Bot Configuration
    LINE_CHANNEL_ACCESS_TOKEN: str = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
    LINE_CHANNEL_SECRET: str = os.getenv("LINE_CHANNEL_SECRET", "")
    
    # Microsoft Graph API (OneDrive)
    MICROSOFT_CLIENT_ID: str = os.getenv("MICROSOFT_CLIENT_ID", "")
    MICROSOFT_CLIENT_SECRET: str = os.getenv("MICROSOFT_CLIENT_SECRET", "")
    MICROSOFT_TENANT_ID: str = os.getenv("MICROSOFT_TENANT_ID", "")
    
    # OpenAI API
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Database Configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # Application Settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    PORT: int = int(os.getenv("PORT", "8000"))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    
    # File Upload Settings
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    ALLOWED_EXTENSIONS: list = os.getenv("ALLOWED_EXTENSIONS", "jpg,jpeg,png,pdf,txt,docx,xlsx").split(",")
    
    # OneDrive Settings
    ONEDRIVE_ROOT_FOLDER: str = os.getenv("ONEDRIVE_ROOT_FOLDER", "LineBot_Uploads")
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate required configuration values"""
        required_fields = [
            "LINE_CHANNEL_ACCESS_TOKEN",
            "LINE_CHANNEL_SECRET",
            "SECRET_KEY"
        ]
        
        missing_fields = []
        for field in required_fields:
            if not getattr(cls, field):
                missing_fields.append(field)
        
        if missing_fields:
            logging.error(f"Missing required configuration: {', '.join(missing_fields)}")
            return False
        
        return True
    
    @classmethod
    def get_log_config(cls) -> dict:
        """Get logging configuration"""
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'detailed': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
                },
                'simple': {
                    'format': '%(levelname)s - %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'level': cls.LOG_LEVEL,
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple'
                },
                'file_info': {
                    'level': 'INFO',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': str(cls.LOGS_DIR / 'app.log'),
                    'maxBytes': 10485760,  # 10MB
                    'backupCount': 5,
                    'formatter': 'detailed'
                },
                'file_error': {
                    'level': 'ERROR',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': str(cls.LOGS_DIR / 'error.log'),
                    'maxBytes': 10485760,  # 10MB
                    'backupCount': 5,
                    'formatter': 'detailed'
                }
            },
            'loggers': {
                '': {  # root logger
                    'handlers': ['console', 'file_info', 'file_error'],
                    'level': cls.LOG_LEVEL,
                    'propagate': False
                }
            }
        }


# Create a global config instance
config = Config()