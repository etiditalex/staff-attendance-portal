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
    
    # Also check for postgres:// (without 'ql') - some systems use this
    if database_url and (database_url.startswith('postgresql://') or database_url.startswith('postgres://')):
        # Convert postgres:// to postgresql:// if needed
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        # Use DATABASE_URL directly if provided by Render
        # URL-encode special characters in password if needed
        try:
            from urllib.parse import quote_plus, urlparse, urlunparse
            parsed = urlparse(database_url)
            if parsed.password:
                # Reconstruct URL with URL-encoded password
                encoded_password = quote_plus(parsed.password)
                new_netloc = f"{parsed.username}:{encoded_password}@{parsed.hostname}"
                if parsed.port:
                    new_netloc += f":{parsed.port}"
                database_url = urlunparse((parsed.scheme, new_netloc, parsed.path, parsed.params, parsed.query, parsed.fragment))
        except Exception as url_err:
            print(f"⚠️ URL encoding warning: {url_err}, using original URL")
        
        SQLALCHEMY_DATABASE_URI = database_url
        print(f"✅ Using DATABASE_URL from Render")
        print(f"   URL preview: {database_url[:70]}..." if len(database_url) > 70 else f"   URL: {database_url[:70]}")
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
    
    # Check if we're on Render - multiple detection methods
    port_var = os.getenv('PORT')
    render_var = os.getenv('RENDER', '').lower()
    is_render = (
        render_var == 'true' or
        port_var is not None or
        'render.com' in str(os.getenv('HOSTNAME', '')).lower()
    )
    
    # Auto-detect PostgreSQL from environment
    db_host_lower = (DB_HOST or '').lower()
    
    # FORCE PostgreSQL if we're on Render (PORT variable is always set on Render)
    if port_var is not None:
        print(f"🚨 DETECTED RENDER ENVIRONMENT (PORT={port_var}) - FORCING POSTGRESQL")
        is_postgres = True
    else:
        # Check other indicators
        is_postgres = (
            SQLALCHEMY_DATABASE_URI is not None or  # Already using DATABASE_URL (PostgreSQL)
            DB_TYPE in ('postgresql', 'postgres') or
            'dpg-' in db_host_lower or 
            'postgres' in db_host_lower or
            db_host_lower.endswith('.render.com') or
            db_host_lower.startswith('dpg-') or
            'postgresql' in db_host_lower
        )
    
    # Debug logging - very detailed
    print(f"🔍 Database Detection Details:")
    print(f"   PORT env var: {port_var or 'NOT SET'}")
    print(f"   RENDER env var: {render_var or 'NOT SET'}")
    print(f"   DB_TYPE: {DB_TYPE or 'not set'}")
    print(f"   DB_HOST: {DB_HOST or 'not set'}")
    print(f"   DB_USER: {DB_USER or 'not set'}")
    print(f"   DB_NAME: {DB_NAME or 'not set'}")
    print(f"   DATABASE_URL: {('SET' if database_url else 'NOT SET')}")
    print(f"   Is Render: {is_render}")
    print(f"   Detected as PostgreSQL: {is_postgres}")
    
    # Build URI if we didn't get DATABASE_URL
    if SQLALCHEMY_DATABASE_URI is None:
        # If on Render, we MUST use PostgreSQL - check if we have the right variables
        if is_render and DB_HOST == 'localhost':
            print("⚠️ WARNING: On Render but DB_HOST is still 'localhost'!")
            print("   This means environment variables from Render aren't being set correctly.")
            print("   Please check Render Dashboard → Environment Variables:")
            print("   - DB_HOST should be your PostgreSQL host (e.g., dpg-xxxxx-xxx)")
            print("   - DB_USER should be your PostgreSQL username")
            print("   - DB_PASSWORD should be your PostgreSQL password")
            print("   - DB_NAME should be your database name")
            print("   - DB_TYPE should be 'postgresql'")
            print("\n   Attempting to use DATABASE_URL as fallback...")
            # Try to get DATABASE_URL as last resort (Render sometimes sets this automatically)
            database_url_fallback = os.getenv('DATABASE_URL', '')
            if database_url_fallback and database_url_fallback.startswith('postgresql://'):
                SQLALCHEMY_DATABASE_URI = database_url_fallback
                print(f"✅ Using DATABASE_URL fallback: {database_url_fallback[:50]}...")
            else:
                # Use a dummy connection string to allow build to complete
                # Will fail at runtime with clear error message
                print("❌ No DATABASE_URL found. Using placeholder - will fail at runtime.")
                print("   Set environment variables in Render Dashboard before using the app.")
                SQLALCHEMY_DATABASE_URI = "postgresql://placeholder:placeholder@placeholder:5432/placeholder"
        elif is_postgres:
            # If on Render but DB_HOST is still localhost, try DATABASE_URL
            if is_render and DB_HOST == 'localhost':
                print("⚠️ On Render but DB_HOST is localhost - trying DATABASE_URL...")
                database_url_fallback = os.getenv('DATABASE_URL', '')
                if database_url_fallback and (database_url_fallback.startswith('postgresql://') or database_url_fallback.startswith('postgres://')):
                    # Convert postgres:// to postgresql:// if needed
                    if database_url_fallback.startswith('postgres://'):
                        database_url_fallback = database_url_fallback.replace('postgres://', 'postgresql://', 1)
                    SQLALCHEMY_DATABASE_URI = database_url_fallback
                    print(f"✅ Using DATABASE_URL: {database_url_fallback[:60]}...")
                else:
                    print("❌ CRITICAL: No database connection available!")
                    print("   You MUST set database environment variables in Render:")
                    print("   - DB_HOST (your PostgreSQL host)")
                    print("   - DB_USER (your PostgreSQL user)")
                    print("   - DB_PASSWORD (your PostgreSQL password)")
                    print("   - DB_NAME (your database name)")
                    print("   OR ensure DATABASE_URL is automatically set by Render")
                    # Use placeholder that will clearly fail
                    SQLALCHEMY_DATABASE_URI = "postgresql://MISSING_VARS:MISSING_VARS@MISSING_VARS:5432/MISSING_VARS"
            else:
                # PostgreSQL connection with provided variables
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



