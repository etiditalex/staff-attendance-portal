"""
Configuration file for Flask Attendance Portal
Loads environment variables and sets up app configurations
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Session Configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)
    
    # Database Configuration (MySQL)
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_NAME = os.getenv('DB_NAME', 'attendance_db')
    
    # SQLAlchemy Configuration
    # Support both MySQL and PostgreSQL
    DB_TYPE = os.getenv('DB_TYPE', '').lower()
    
    # Auto-detect PostgreSQL (Render PostgreSQL URLs contain 'dpg-' or 'postgres')
    is_postgres = (DB_TYPE == 'postgresql' or 
                  DB_TYPE == 'postgres' or
                  'dpg-' in DB_HOST.lower() or 
                  'postgres' in DB_HOST.lower() or
                  DB_HOST.endswith('.render.com'))
    
    if is_postgres:
        # PostgreSQL connection
        password_part = f":{DB_PASSWORD}@" if DB_PASSWORD else "@"
        # PostgreSQL uses format: postgresql://user:password@host:port/database
        # Render provides host without port, SQLAlchemy uses default 5432
        SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}{password_part}{DB_HOST}/{DB_NAME}"
        print(f"✅ Using PostgreSQL: {DB_HOST}/{DB_NAME}")
    else:
        # MySQL connection (default)
        password_part = f":{DB_PASSWORD}@" if DB_PASSWORD else "@"
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}{password_part}{DB_HOST}/{DB_NAME}?charset=utf8mb4"
        print(f"✅ Using MySQL: {DB_HOST}/{DB_NAME}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set to True for SQL debugging
    
    # Twilio WhatsApp Configuration
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', '')  # Format: whatsapp:+1234567890
    
    # Application Configuration
    ATTENDANCE_CUTOFF_TIME = os.getenv('ATTENDANCE_CUTOFF_TIME', '09:00')  # 9:00 AM cutoff
    ITEMS_PER_PAGE = 20
    
    # File Upload Configuration (for future extensions)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = False  # Disabled for faster startup

class ProductionConfig(Config):
    """Production environment configuration"""
    DEBUG = False
    # In production, ensure all sensitive data comes from environment variables
    
class TestingConfig(Config):
    """Testing environment configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}



