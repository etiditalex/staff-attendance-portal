"""
Fast startup script - skips slow initialization
"""
import os
import sys

# Disable slow SQLAlchemy logging
os.environ['SQLALCHEMY_ECHO'] = 'False'

print("\n" + "=" * 60)
print("🚀 Starting Attendance Portal (Fast Mode)")
print("=" * 60)

# Import and run
try:
    from app import app
    print("\n✅ App loaded successfully!")
    print("\n📊 Application will start at: http://localhost:5000")
    print("📧 Default admin: admin@attendance.com / admin123")
    print("\n💡 Press CTRL+C to stop\n")
    print("=" * 60 + "\n")
    
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False, threaded=True)
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to exit...")


