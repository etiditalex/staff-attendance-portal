"""
Quick test to see what's blocking
"""
print("Testing imports...")
try:
    from app import app
    print("✅ App imported successfully")
except Exception as e:
    print(f"❌ Error importing app: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\nTesting database connection...")
try:
    with app.app_context():
        from models.db import db
        db.engine.connect()
        print("✅ Database connected")
except Exception as e:
    print(f"❌ Database error: {e}")
    exit(1)

print("\n✅ Everything looks good! Starting server...")
print("=" * 60)
print("Starting Flask app on http://localhost:5000")
print("Press CTRL+C to stop")
print("=" * 60)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)


