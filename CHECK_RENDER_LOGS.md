# 🔍 How to Check Render Logs for Errors

## Steps to Find the Exact Error

1. **Go to Render Dashboard**
   - Login to https://render.com
   - Click on your **Web Service** (`staff-attendance-portal`)

2. **Check Logs Tab**
   - Click on **"Logs"** tab at the top
   - Scroll down to see recent errors
   - Look for red error messages

3. **Look for Python Tracebacks**
   - Errors will show in red
   - Look for lines starting with:
     - `Traceback (most recent call last)`
     - `File "`
     - `Error:`
     - `Exception:`

4. **Common Errors to Look For:**
   - `TypeError` - Wrong data type
   - `OperationalError` - Database connection issue
   - `ProgrammingError` - SQL syntax issue
   - `AttributeError` - Missing attribute
   - `ImportError` - Missing module

---

## What to Share

If you find the error, please share:
1. The **full error message** (copy from logs)
2. Any **traceback** lines
3. The **last few log lines** before the error

This will help me fix it quickly!

