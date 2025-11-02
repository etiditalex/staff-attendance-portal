"""
Database models for Staff Attendance Portal
Defines User, Attendance, and Notification models using SQLAlchemy ORM
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import pytz
import os

# Initialize SQLAlchemy with connection pooling
db = SQLAlchemy()

# Detect database type for Enum handling
def get_db_type():
    """Detect if using PostgreSQL or MySQL from environment"""
    db_host = os.getenv('DB_HOST', '').lower()
    db_type = os.getenv('DB_TYPE', '').lower()
    
    # Check multiple indicators
    if (db_type in ('postgresql', 'postgres') or 
        'postgres' in db_host or 
        'dpg-' in db_host or 
        db_host.endswith('.render.com')):
        return 'postgresql'
    return 'mysql'

# Detect at module load (will be re-evaluated in app context)
def is_postgresql():
    """Check if using PostgreSQL - call after app config loaded"""
    try:
        from flask import current_app
        db_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI', '')
        return 'postgresql' in db_uri.lower() or 'postgres' in db_uri.lower()
    except:
        # Fallback to environment variable check
        db_host = os.getenv('DB_HOST', '').lower()
        return 'postgres' in db_host or 'dpg-' in db_host

# Use String for all (PostgreSQL compatible) - ENUM causes issues
# SQLAlchemy will handle validation in application code
USE_ENUM = False  # Disable ENUM for PostgreSQL compatibility

# Helper function to handle connection errors
def get_db_session():
    """Get database session with auto-reconnect"""
    try:
        return db.session
    except Exception:
        db.session.rollback()
        return db.session

class User(UserMixin, db.Model):
    """User model for staff and admin accounts"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    # Use String for PostgreSQL compatibility (ENUM causes issues)
    role = db.Column(db.String(20), default='staff', nullable=False)
    status = db.Column(db.String(20), default='active', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendances = db.relationship('Attendance', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user has admin role"""
        return self.role == 'admin'
    
    def get_today_attendance(self):
        """Get today's attendance record"""
        today = date.today()
        return Attendance.query.filter_by(user_id=self.id, date=today).first()
    
    def get_attendance_summary(self, days=7):
        """Get attendance summary for the last N days"""
        from sqlalchemy import func
        from datetime import timedelta
        
        try:
            start_date = date.today() - timedelta(days=days-1)
            
            # Get all attendance records in the period
            records = Attendance.query.filter(
                Attendance.user_id == self.id,
                Attendance.date >= start_date
            ).all()
            
            # Count by status
            summary = {
                'total_days': len(records),
                'present_days': 0,
                'remote_days': 0,
                'leave_days': 0,
                'absent_days': 0
            }
            
            for record in records:
                if record.status == 'Present' and record.work_type == 'Remote':
                    summary['remote_days'] += 1
                elif record.status == 'Present':
                    summary['present_days'] += 1
                elif record.status == 'Leave':
                    summary['leave_days'] += 1
                elif record.status == 'Absent':
                    summary['absent_days'] += 1
            
            return summary
        except Exception as e:
            # Return empty summary if query fails
            print(f"⚠️ Error getting attendance summary: {e}")
            return {
                'total_days': 0,
                'present_days': 0,
                'remote_days': 0,
                'leave_days': 0,
                'absent_days': 0
            }
    
    def __repr__(self):
        return f'<User {self.email}>'


class Attendance(db.Model):
    """Attendance model for tracking daily login/logout"""
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, default=date.today, index=True)
    login_time = db.Column(db.DateTime, nullable=True)
    logout_time = db.Column(db.DateTime, nullable=True)
    # Use String for PostgreSQL compatibility (no ENUM)
    status = db.Column(db.String(20), default='Absent', nullable=False)
    work_type = db.Column(db.String(20), default='Office', nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Composite unique constraint to prevent duplicate entries per user per day
    __table_args__ = (
        db.UniqueConstraint('user_id', 'date', name='unique_user_date'),
    )
    
    def mark_login(self):
        """Mark login time and update status"""
        self.login_time = datetime.now()
        self.status = 'Present'
        db.session.commit()
    
    def mark_logout(self):
        """Mark logout time"""
        self.logout_time = datetime.now()
        db.session.commit()
    
    def get_work_duration(self):
        """Calculate work duration in hours"""
        if self.login_time and self.logout_time:
            duration = self.logout_time - self.login_time
            return round(duration.total_seconds() / 3600, 2)
        return None
    
    def format_time(self, dt):
        """Format datetime to readable string"""
        if dt:
            return dt.strftime('%I:%M %p')
        return 'N/A'
    
    @staticmethod
    def get_absent_users(target_date=None):
        """Get list of users who haven't logged in for a specific date"""
        if target_date is None:
            target_date = date.today()
        
        # Get all active users
        all_users = User.query.filter_by(status='active').all()
        
        # Get users who have attendance record for the date
        present_user_ids = db.session.query(Attendance.user_id).filter(
            Attendance.date == target_date,
            Attendance.status != 'Absent'
        ).all()
        present_user_ids = [uid[0] for uid in present_user_ids]
        
        # Return users not in present list
        return [user for user in all_users if user.id not in present_user_ids]
    
    def __repr__(self):
        return f'<Attendance User:{self.user_id} Date:{self.date} Status:{self.status}>'


class Notification(db.Model):
    """Notification model for tracking WhatsApp messages"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    # Use String for PostgreSQL compatibility (no ENUM)
    type = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='pending', nullable=False)
    sent_at = db.Column(db.DateTime, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def mark_sent(self):
        """Mark notification as sent"""
        self.status = 'sent'
        self.sent_at = datetime.now()
        db.session.commit()
    
    def mark_failed(self, error):
        """Mark notification as failed"""
        self.status = 'failed'
        self.error_message = str(error)
        db.session.commit()
    
    def __repr__(self):
        return f'<Notification {self.type} for User:{self.user_id}>'


class WebAuthnCredential(db.Model):
    """WebAuthn/FIDO2 credentials for biometric authentication"""
    __tablename__ = 'webauthn_credentials'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    credential_id = db.Column(db.Text, nullable=False, unique=True)  # Base64 encoded
    public_key = db.Column(db.Text, nullable=False)  # JSON string of public key
    counter = db.Column(db.BigInteger, default=0, nullable=False)
    device_name = db.Column(db.String(100), nullable=True)  # e.g., "iPhone 13", "Chrome on Windows"
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    user = db.relationship('User', backref='webauthn_credentials')
    
    def __repr__(self):
        return f'<WebAuthnCredential {self.device_name} for User:{self.user_id}>'


def init_db(app):
    """Initialize database with app context"""
    db.init_app(app)
    
    with app.app_context():
        # Configure connection pool settings if provided in config
        try:
            engine_options = app.config.get('SQLALCHEMY_ENGINE_OPTIONS', {})
            if engine_options:
                # Apply engine options if SQLAlchemy supports it
                # Flask-SQLAlchemy automatically applies SQLALCHEMY_ENGINE_OPTIONS
                print(f"✅ Database engine options configured")
        except:
            pass
        
        # Test connection once
        try:
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            db.session.commit()
            print("✅ Initial database connection test passed")
        except Exception as conn_test:
            print(f"⚠️ Initial connection test failed: {conn_test}")
            db.session.rollback()
        
        try:
            # Check if tables exist first (faster than create_all)
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            # Only create tables if they don't exist (saves time)
            if 'users' not in existing_tables:
                db.create_all()
        except Exception as e:
            # If check fails, create tables anyway
            try:
                db.create_all()
            except:
                pass
        
        # Create default admin user if not exists
        try:
            admin = User.query.filter_by(email='admin@attendance.com').first()
            if not admin:
                admin = User(
                    name='Admin User',
                    email='admin@attendance.com',
                    phone='+1234567890',
                    department='Administration',
                    role='admin',
                    status='active'
                )
                admin.set_password('admin123')  # Change this in production
                db.session.add(admin)
                db.session.commit()
                print("✅ Default admin user created: admin@attendance.com / admin123")
        except Exception as e:
            # User table might not exist yet or connection issue
            print(f"⚠️ Could not create admin user: {e}")
            # Make sure tables exist first
            try:
                db.create_all()
                # Try creating admin again
                try:
                    admin = User.query.filter_by(email='admin@attendance.com').first()
                    if not admin:
                        admin = User(
                            name='Admin User',
                            email='admin@attendance.com',
                            phone='+1234567890',
                            department='Administration',
                            role='admin',
                            status='active'
                        )
                        admin.set_password('admin123')
                        db.session.add(admin)
                        db.session.commit()
                        print("✅ Default admin user created: admin@attendance.com / admin123")
                except:
                    pass
            except:
                pass



