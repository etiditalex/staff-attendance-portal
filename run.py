#!/usr/bin/env python
"""
Quick start script for Staff Attendance Portal
This script provides a convenient way to run the application
"""
import os
import sys

def main():
    """Main function to run the Flask application"""
    
    print("=" * 60)
    print("  🚀 Starting Staff Attendance Portal")
    print("=" * 60)
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("\n⚠️  WARNING: .env file not found!")
        print("   Please create a .env file from env.example")
        print("   Copy env.example to .env and configure your settings\n")
        
        response = input("Do you want to continue anyway? (y/n): ").lower()
        if response != 'y':
            print("\n❌ Exiting. Please create .env file first.")
            sys.exit(1)
    
    # Check if required packages are installed
    try:
        import flask
        import flask_sqlalchemy
        import flask_login
        import pymysql
        from dotenv import load_dotenv
    except ImportError as e:
        print(f"\n❌ Missing required package: {e.name}")
        print("\n📦 Please install requirements:")
        print("   pip install -r requirements.txt\n")
        sys.exit(1)
    
    print("\n✅ All checks passed!")
    print("\n📊 Application will start at: http://localhost:5000")
    print("📧 Default admin: admin@attendance.com / admin123")
    print("\n💡 Press CTRL+C to stop the server\n")
    print("=" * 60)
    
    # Import and run the app
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()




