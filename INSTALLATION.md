# 📦 Installation Guide - Staff Attendance Portal

Complete step-by-step installation guide for the Staff Attendance Portal.

---

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Windows Installation](#windows-installation)
3. [Linux Installation](#linux-installation)
4. [macOS Installation](#macos-installation)
5. [Database Setup](#database-setup)
6. [Configuration](#configuration)
7. [Running the Application](#running-the-application)
8. [Troubleshooting](#troubleshooting)

---

## 🖥️ System Requirements

### Minimum Requirements
- **Operating System**: Windows 10, Ubuntu 20.04+, macOS 10.15+
- **Python**: 3.8 or higher
- **MySQL**: 8.0 or higher
- **RAM**: 2GB minimum
- **Disk Space**: 500MB free space

### Recommended Requirements
- **Python**: 3.10+
- **MySQL**: 8.0+
- **RAM**: 4GB or more
- **Internet**: For WhatsApp notifications (Twilio)

---

## 🪟 Windows Installation

### Step 1: Install Python

1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. ✅ **IMPORTANT**: Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
```cmd
python --version
```

### Step 2: Install MySQL

1. Download MySQL from https://dev.mysql.com/downloads/installer/
2. Choose "MySQL Installer Community"
3. Install MySQL Server (default settings)
4. Remember the root password you set
5. Verify installation:
```cmd
mysql --version
```

### Step 3: Setup Project

Open Command Prompt or PowerShell:

```cmd
# Navigate to project directory
cd C:\path\to\attendance_portal

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Database

```cmd
# Login to MySQL
mysql -u root -p

# Run the schema
source schema.sql
# OR
exit
mysql -u root -p < schema.sql
```

### Step 5: Setup Environment

```cmd
# Copy example file
copy env.example .env

# Edit .env with Notepad
notepad .env
```

Configure your settings:
```env
SECRET_KEY=your-random-secret-key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=attendance_db
```

### Step 6: Run Application

```cmd
# Make sure virtual environment is activated
venv\Scripts\activate

# Run the app
python app.py

# OR use the run script
python run.py
```

Visit: http://localhost:5000

---

## 🐧 Linux Installation

### Step 1: Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 2: Install Python & Dependencies

```bash
# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv -y

# Install MySQL
sudo apt install mysql-server -y

# Verify installations
python3 --version
mysql --version
```

### Step 3: Setup MySQL

```bash
# Secure MySQL installation
sudo mysql_secure_installation

# Login to MySQL
sudo mysql

# Create database user (optional)
CREATE USER 'attendance_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON attendance_db.* TO 'attendance_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 4: Setup Project

```bash
# Navigate to project
cd /path/to/attendance_portal

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 5: Configure Database

```bash
# Import schema
mysql -u root -p < schema.sql

# Or login and source
mysql -u root -p
source schema.sql
exit
```

### Step 6: Setup Environment

```bash
# Copy example file
cp env.example .env

# Edit with nano or vim
nano .env
```

Configure your settings:
```env
SECRET_KEY=your-random-secret-key
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=attendance_db
```

### Step 7: Run Application

```bash
# Activate virtual environment if not already
source venv/bin/activate

# Run the app
python3 app.py

# OR use the run script
python3 run.py
```

Visit: http://localhost:5000

### Optional: Run as Service

Create systemd service file:

```bash
sudo nano /etc/systemd/system/attendance.service
```

Add:
```ini
[Unit]
Description=Staff Attendance Portal
After=network.target

[Service]
User=your-username
WorkingDirectory=/path/to/attendance_portal
Environment="PATH=/path/to/attendance_portal/venv/bin"
ExecStart=/path/to/attendance_portal/venv/bin/python app.py

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable attendance
sudo systemctl start attendance
sudo systemctl status attendance
```

---

## 🍎 macOS Installation

### Step 1: Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Python & MySQL

```bash
# Install Python
brew install python@3.10

# Install MySQL
brew install mysql

# Start MySQL service
brew services start mysql

# Verify installations
python3 --version
mysql --version
```

### Step 3: Setup MySQL

```bash
# Secure MySQL
mysql_secure_installation

# Login to MySQL
mysql -u root -p
```

### Step 4: Setup Project

```bash
# Navigate to project
cd /path/to/attendance_portal

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 5: Configure Database

```bash
# Import schema
mysql -u root -p < schema.sql
```

### Step 6: Setup Environment

```bash
# Copy example file
cp env.example .env

# Edit with nano or TextEdit
nano .env
```

### Step 7: Run Application

```bash
# Activate virtual environment
source venv/bin/activate

# Run the app
python3 app.py
```

Visit: http://localhost:5000

---

## 🗄️ Database Setup

### Method 1: Using MySQL Command Line

```bash
# Login to MySQL
mysql -u root -p

# Run the schema
source /path/to/schema.sql

# Verify tables
USE attendance_db;
SHOW TABLES;
```

### Method 2: Using MySQL Workbench

1. Open MySQL Workbench
2. Connect to your MySQL server
3. File → Open SQL Script
4. Select `schema.sql`
5. Execute (⚡ icon)

### Method 3: Using phpMyAdmin

1. Open phpMyAdmin in browser
2. Create database `attendance_db`
3. Import → Choose `schema.sql`
4. Click "Go"

---

## ⚙️ Configuration

### 1. Environment Variables (.env)

```env
# Flask Settings
SECRET_KEY=generate-a-random-key-here
FLASK_ENV=development

# Database Settings
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=attendance_db

# Twilio WhatsApp Settings (Optional)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# App Settings
ATTENDANCE_CUTOFF_TIME=09:00
```

### 2. Generate Secret Key

```python
# Run in Python
import secrets
print(secrets.token_hex(32))
```

Or:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Twilio WhatsApp Setup (Optional)

1. Sign up at https://www.twilio.com/try-twilio
2. Go to Console → Messaging → WhatsApp sandbox
3. Follow instructions to join sandbox
4. Copy credentials to `.env`

**Note**: WhatsApp is optional. App works without it.

---

## 🚀 Running the Application

### Development Mode

```bash
# Activate virtual environment first
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Run the app
python app.py

# OR use run script
python run.py
```

### Production Mode (Gunicorn)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### With Custom Port

```bash
# Edit app.py, change last line:
app.run(debug=True, host='0.0.0.0', port=8080)
```

---

## 🔧 Troubleshooting

### Problem: "ModuleNotFoundError"

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install requirements
pip install -r requirements.txt
```

### Problem: "Access denied for user"

**Solution**:
- Check MySQL username and password in `.env`
- Verify MySQL is running: `mysql --version`
- Test connection: `mysql -u root -p`

### Problem: "Can't connect to MySQL server"

**Solution**:
```bash
# Start MySQL service

# Linux
sudo systemctl start mysql

# macOS
brew services start mysql

# Windows
net start MySQL80
```

### Problem: "Port 5000 already in use"

**Solution**:
```bash
# Find and kill the process (Linux/Mac)
lsof -ti:5000 | xargs kill -9

# Or change port in app.py
app.run(debug=True, port=5001)
```

### Problem: "Template not found"

**Solution**:
- Ensure you're running from project root directory
- Check `templates/` folder exists
- Verify all HTML files are present

### Problem: WhatsApp not sending

**Solution**:
- Verify Twilio credentials in `.env`
- Check phone number format: `+1234567890`
- Join Twilio WhatsApp sandbox
- App works without WhatsApp (notifications just fail)

---

## ✅ Verify Installation

After setup, verify everything works:

1. **Database Connection**:
```bash
mysql -u root -p
USE attendance_db;
SHOW TABLES;
# Should show: users, attendance, notifications
```

2. **Application Start**:
```bash
python app.py
# Should show: Running on http://127.0.0.1:5000
```

3. **Access Application**:
- Open browser: http://localhost:5000
- Should see login page

4. **Admin Login**:
- Email: `admin@attendance.com`
- Password: `admin123`
- Should access admin panel

---

## 📞 Need Help?

If you encounter issues:
1. Check error messages carefully
2. Review this guide again
3. Check `README.md` for more info
4. Search error messages online
5. Contact your development team

---

**Installation Complete! 🎉**

Proceed to use the application or refer to README.md for usage instructions.




