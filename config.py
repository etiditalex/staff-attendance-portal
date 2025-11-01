"""
Configuration file for Flask Attendance Portal
Loads environment variables and sets up app configurations
"""
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file (only if not on Render)
# On Render, environment variables are set by Render, not .env file
if not os.getenv('RENDER'):
    load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Session Configuration
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=12)
    
    # Database Configuration
    # Check for Render's default database environment variables first
    # Render sets DATABASE_URL for PostgreSQL automatically
    database_url = os.getenv('DATABASE_URL', '')
    
    # Initialize variables (will be set in if/else below)
    DB_HOST = None
    DB_USER = None
    DB_PASSWORD = None
    DB_NAME = None
    SQLALCHEMY_DATABASE_URI = None
    
    if database_url and database_url.startswith('postgresql://'):
        # Use DATABASE_URL directly if provided by Render
        SQLALCHEMY_DATABASE_URI = database_url
        print(f"✅ Using DATABASE_URL from Render")
        # Extract values for display/debugging
        try:
            import re
            match = re.match(r'postgresql://([^:]+):([^@]+)@([^:]+):?(\d+)?/(.+)', database_url)
            if match:
                DB_USER = match.group(1)
                DB_HOST = match.group(3)
                DB_NAME = match.group(5)
                DB_PASSWORD = "***"  # Don't log password
        except:
            pass
    else:
        # Use individual environment variables
        DB_HOST = os.getenv('DB_HOST', 'localhost')
        DB_USER = os.getenv('DB_USER', 'root')
        DB_PASSWORD = os.getenv('DB_PASSWORD', '')
        DB_NAME = os.getenv('DB_NAME', 'attendance_db')
    
    # SQLAlchemy Configuration
    # Support both MySQL and PostgreSQL
    DB_TYPE = os.getenv('DB_TYPE', '').lower()
    
    # Check if we're on Render
    # Render sets RENDER=true OR we can detect by PORT environment variable
    is_render = (
        os.getenv('RENDER', '').lower() == 'true' or
        os.getenv('PORT') is not None  # Render always sets PORT
    )
    
    # Auto-detect PostgreSQL from environment
    # Check if DB_HOST looks like a Render PostgreSQL host (contains 'dpg-' or ends with '.render.com')
    # OR if DB_TYPE is explicitly set to postgresql/postgres
    # OR if we're on Render (force PostgreSQL on Render)
    db_host_lower = (DB_HOST or '').lower()
    is_postgres = (
        SQLALCHEMY_DATABASE_URI is not None or  # Already using DATABASE_URL (PostgreSQL)
        DB_TYPE in ('postgresql', 'postgres') or
        is_render or  # Force PostgreSQL on Render
        'dpg-' in db_host_lower or 
        'postgres' in db_host_lower or
        db_host_lower.endswith('.render.com') or
        db_host_lower.startswith('dpg-') or
        'postgresql' in db_host_lower
    )
    
    # Debug logging
    print(f"🔍 Database Detection:")
    print(f"   DB_TYPE: {DB_TYPE or 'not set'}")
    print(f"   DB_HOST: {DB_HOST or 'not set'}")
    print(f"   Is Render: {is_render}")
    print(f"   Detected as PostgreSQL: {is_postgres}")
    
    # Build URI if we didn't get DATABASE_URL
    if SQLALCHEMY_DATABASE_URI is None:
        if is_postgres:
            # PostgreSQL connection
            password_part = f":{DB_PASSWORD}@" if DB_PASSWORD else "@"
            # PostgreSQL uses format: postgresql://user:password@host:port/database
            # Render provides host without port, SQLAlchemy uses default 5432
            SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}{password_part}{DB_HOST}/{DB_NAME}"
            print(f"✅ Using PostgreSQL: {DB_USER}@{DB_HOST}/{DB_NAME}")
        else:
            # MySQL connection (default for local development)
            password_part = f":{DB_PASSWORD}@" if DB_PASSWORD else "@"
            SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}{password_part}{DB_HOST}/{DB_NAME}?charset=utf8mb4"
            print(f"✅ Using MySQL: {DB_USER}@{DB_HOST}/{DB_NAME}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # Set to True for SQL debugging
    
    # Twilio WhatsApp Configuration
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', '')  # Format: whatsapp:+1234567890
    
    # Email Configuration (SMTP)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME', ''))
    MAIL_SUBJECT_PREFIX = '[Attendance Portal] '
    
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



