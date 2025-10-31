"""
Database initialization script for production deployment
Run this after deploying to Render or any cloud platform
"""
import os
import sys
from app import app, db
from models.db import User

def init_database():
    """Initialize database with tables and default admin user"""
    print("=" * 60)
    print("🔧 Initializing Database...")
    print("=" * 60)
    
    with app.app_context():
        try:
            # Create all tables
            print("\n📊 Creating database tables...")
            db.create_all()
            print("✅ Tables created successfully!")
            
            # Check if admin exists
            admin = User.query.filter_by(email='admin@attendance.com').first()
            
            if not admin:
                print("\n👤 Creating default admin user...")
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
                print("✅ Admin user created!")
                print("   Email: admin@attendance.com")
                print("   Password: admin123")
                print("   ⚠️  IMPORTANT: Change password after first login!")
            else:
                print("\n✅ Admin user already exists")
            
            print("\n" + "=" * 60)
            print("🎉 Database initialization complete!")
            print("=" * 60)
            return True
            
        except Exception as e:
            print(f"\n❌ Error initializing database: {str(e)}")
            return False

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)



