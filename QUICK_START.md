# ⚡ Quick Start Guide - Staff Attendance Portal

Get up and running in 5 minutes!

---

## 🚀 Super Fast Setup (Development)

### 1️⃣ Install Python & MySQL
Make sure you have:
- Python 3.8+ installed
- MySQL 8.0+ installed and running

### 2️⃣ Clone & Setup
```bash
# Navigate to project folder
cd attendance_portal

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3️⃣ Setup Database
```bash
# Login to MySQL
mysql -u root -p

# Import schema
source schema.sql
# Or: mysql -u root -p < schema.sql

# Exit
exit
```

### 4️⃣ Configure Environment
```bash
# Copy example file
cp env.example .env    # Mac/Linux
copy env.example .env  # Windows

# Edit .env file with your MySQL password
# Required: DB_PASSWORD=your_mysql_password
# Optional: Twilio credentials (for WhatsApp)
```

### 5️⃣ Run Application
```bash
python run.py
```

### 6️⃣ Access Application
Open browser: **http://localhost:5000**

**Default Admin Login:**
- Email: `admin@attendance.com`
- Password: `admin123`

---

## 🎯 What You Get

### For Staff:
- ✅ Sign up with your details
- ✅ Login = Auto-records your arrival time
- ✅ Logout = Auto-records your departure time
- ✅ View your attendance history
- ✅ Request leave or mark remote work
- ✅ WhatsApp notifications (if configured)

### For Admin:
- ✅ View all staff attendance
- ✅ See who's absent today
- ✅ Filter by date, department, status
- ✅ Export data to CSV
- ✅ Real-time statistics

---

## 🔧 Minimal .env Configuration

```env
# Essential Settings (Minimum Required)
SECRET_KEY=change-this-to-random-string
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=attendance_db

# Optional (Leave blank for testing)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_WHATSAPP_NUMBER=
```

---

## 🆘 Troubleshooting

### "Can't connect to MySQL"
```bash
# Make sure MySQL is running
# Windows: net start MySQL80
# Linux: sudo systemctl start mysql
# Mac: brew services start mysql
```

### "Module not found"
```bash
# Make sure virtual environment is activated
# Then reinstall:
pip install -r requirements.txt
```

### "Port 5000 already in use"
Edit `app.py`, change the last line:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### "Access denied for user"
Check your `.env` file:
- `DB_USER` should match your MySQL username
- `DB_PASSWORD` should match your MySQL password

---

## 📱 WhatsApp Setup (Optional)

### Quick Test with Twilio Sandbox

1. Sign up: https://www.twilio.com/try-twilio (Free)
2. Go to: Console → Messaging → Try WhatsApp
3. Send message to Twilio number: `join [your-sandbox-keyword]`
4. Copy credentials to `.env`:
   ```env
   TWILIO_ACCOUNT_SID=your_sid_here
   TWILIO_AUTH_TOKEN=your_token_here
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   ```
5. Restart app

**Note**: Without WhatsApp, app works perfectly! Notifications just won't send.

---

## 🎓 Test the Application

### Create a Test Staff Account
1. Go to: http://localhost:5000/signup
2. Fill in details:
   - Name: John Doe
   - Email: john@test.com
   - Phone: +1234567890
   - Department: Engineering
   - Password: test123
3. Click "Create Account"

### Test Login/Logout Flow
1. Login with john@test.com / test123
2. Check dashboard - login time recorded!
3. Click logout - logout time recorded!
4. Login again to see your attendance history

### Test Admin Panel
1. Logout from staff account
2. Login with: admin@attendance.com / admin123
3. See all attendance records
4. Try filtering by date or department
5. Export data to CSV

---

## 📊 Database Quick Check

```bash
# Login to MySQL
mysql -u root -p

# Use database
USE attendance_db;

# Check tables
SHOW TABLES;

# View users
SELECT id, name, email, role FROM users;

# View today's attendance
SELECT * FROM attendance WHERE date = CURDATE();

# Exit
exit
```

---

## 🚀 Deploy to Production

For production deployment, see:
- **DEPLOYMENT.md** - Complete deployment guides
- Supports: Render, PythonAnywhere, Heroku, AWS, DigitalOcean, Docker

Quick recommendation: **Render.com** (easiest, free tier available)

---

## 📚 Need More Help?

- **Full Documentation**: README.md
- **Installation Guide**: INSTALLATION.md
- **Deployment Guide**: DEPLOYMENT.md
- **Project Summary**: PROJECT_SUMMARY.md

---

## 🎉 You're Ready!

The application is now running. Start marking attendance!

**Tips:**
- Change admin password immediately
- Staff members should sign up with their real phone numbers (for WhatsApp)
- Check dashboard daily to see who's present/absent
- Export data monthly for records

---

**Have fun with your new attendance system! 🚀**




