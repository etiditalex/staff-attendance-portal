"""Quick MySQL connection test"""
import pymysql

print("Testing MySQL connection...")

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='attendance_db',
        connect_timeout=5
    )
    print("✅ MySQL connection successful!")
    conn.close()
except Exception as e:
    print(f"❌ MySQL connection failed: {e}")
    print("\nPossible fixes:")
    print("1. Make sure Laragon MySQL is running (green)")
    print("2. Check if MySQL has a password (update .env)")
    print("3. Verify database 'attendance_db' exists")


