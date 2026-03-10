"""Flask application configuration using python-dotenv."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class."""

    # Application Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    APP_NAME = '穿搭AI'

    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ootd.db')

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24 * 7  # 7 days in seconds
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'

    # Tongyi Wanxiang API
    TONGYI_API_KEY = os.getenv('TONGYI_API_KEY', '')

    # Alibaba Cloud OSS Configuration
    OSS_REGION = os.getenv('OSS_REGION', '')
    OSS_ACCESS_KEY_ID = os.getenv('OSS_ACCESS_KEY_ID', '')
    OSS_ACCESS_KEY_SECRET = os.getenv('OSS_ACCESS_KEY_SECRET', '')
    OSS_BUCKET = os.getenv('OSS_BUCKET', '')

    # Upload Configuration
    UPLOAD_DIR = os.getenv('UPLOAD_DIR', '/data/public/uploads')
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif']


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATABASE_URL = 'sqlite:///test_ootd.db'


# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env_name=None):
    """Get configuration based on environment name."""
    if env_name is None:
        env_name = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env_name, DevelopmentConfig)
