# 🔧 Initialize Database on Render

## Quick Fix: Initialize Database via Render Shell

Since your deployment is successful but signup fails, you need to initialize the database tables.

### Option 1: Use Render Shell (Recommended)

1. Go to your Render Web Service dashboard
2. Click on "Shell" tab (or "Shell" button)
3. Run this command:
   ```bash
   python init_db.py
   ```
4. You should see: "✅ Tables created" and "✅ Default admin user created"
5. Try signing up again!

### Option 2: Auto-Initialize on First Request

The app has been updated to auto-create tables on first signup attempt, but if it still fails, use Option 1.

---

## What to Check

If signup still fails:
1. Check Render logs for the exact error
2. Verify database environment variables are set correctly
3. Make sure PostgreSQL database is running

---

## Test After Initialization

1. **Login as Admin:**
   - Email: `admin@attendance.com`
   - Password: `admin123`

2. **Create Staff Account:**
   - Sign up with a new email
   - Should work now!




