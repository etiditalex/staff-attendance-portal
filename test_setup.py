"""
Quick test script to verify setup
"""
import sys
import os

print("=" * 60)
print("Testing Setup...")
print("=" * 60)

# Test 1: Python version
print("\n1. Checking Python version...")
try:
    import sys
    print(f"   ✅ Python {sys.version}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Check imports
print("\n2. Checking Flask installation...")
try:
    import flask
    print(f"   ✅ Flask {flask.__version__}")
except ImportError as e:
    print(f"   ❌ Flask not installed: {e}")
    sys.exit(1)

# Test 3: Check database connection
print("\n3. Testing database connection...")
try:
    from config import config
    from models.db import db, User
    from app import app
    
    with app.app_context():
        # Try to connect
        db.engine.connect()
        print("   ✅ Database connection successful!")
        
        # Check if tables exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        if 'users' in tables:
            print(f"   ✅ Tables found: {', '.join(tables)}")
        else:
            print(f"   ⚠️  Tables not found. Run: python init_db.py")
            
except Exception as e:
    print(f"   ❌ Database connection failed: {e}")
    print("\n   Possible fixes:")
    print("   - Make sure Laragon MySQL is running")
    print("   - Check .env file has correct DB settings")
    print("   - Verify database 'attendance_db' exists")

# Test 4: Check .env file
print("\n4. Checking .env file...")
if os.path.exists('.env'):
    print("   ✅ .env file exists")
    with open('.env', 'r') as f:
        content = f.read()
        if 'DB_NAME=attendance_db' in content:
            print("   ✅ Database name configured")
        if 'DB_HOST=localhost' in content:
            print("   ✅ Database host configured")
else:
    print("   ⚠️  .env file not found. Run: copy env.example .env")

print("\n" + "=" * 60)
print("Setup test complete!")
print("=" * 60)



