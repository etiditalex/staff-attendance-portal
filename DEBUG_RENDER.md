# 🔍 Debug Render Deployment Issues

## Step 1: Check Render Logs

1. Go to your Render dashboard
2. Click on your Web Service
3. Click "Logs" tab
4. Look for error messages (usually in red)
5. Copy the full error message and share it

## Step 2: Test Database Connection

Visit this URL in your browser:
```
https://your-app-name.onrender.com/health
```

This will show:
- Database connection status
- Any connection errors

## Step 3: Common Errors & Fixes

### Error: "relation does not exist" or "table does not exist"
**Solution:** Database tables not created yet
- The app should auto-create them
- If not, check environment variables

### Error: "connection refused" or "timeout"
**Solution:** Database connection issue
- Verify DB_HOST, DB_USER, DB_PASSWORD in environment variables
- Check PostgreSQL database is running in Render

### Error: "ENUM" or "type mismatch"
**Solution:** Should be fixed now (all ENUMs removed)

---

## Quick Test URLs

1. **Health Check:**
   ```
   https://your-app.onrender.com/health
   ```

2. **Homepage:**
   ```
   https://your-app.onrender.com/
   ```

3. **Login:**
   ```
   https://your-app.onrender.com/login
   ```

---

## What to Share

Please share:
1. The exact error from Render Logs
2. What you see when visiting `/health` endpoint
3. Which page gives the error (signup, login, etc.)

