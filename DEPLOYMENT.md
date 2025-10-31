# 🚀 Deployment Guide - Staff Attendance Portal

Complete deployment guide for various hosting platforms.

---

## 📋 Table of Contents
1. [Render Deployment](#render-deployment)
2. [PythonAnywhere Deployment](#pythonanywhere-deployment)
3. [Heroku Deployment](#heroku-deployment)
4. [AWS EC2 Deployment](#aws-ec2-deployment)
5. [DigitalOcean Deployment](#digitalocean-deployment)
6. [Docker Deployment](#docker-deployment)

---

## 🎨 Render Deployment (Recommended)

Render offers free tier with MySQL database support.

### Step 1: Prepare Repository

1. Push code to GitHub/GitLab
2. Add `gunicorn` to `requirements.txt`:
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

3. Create `render.yaml` in project root:
```yaml
databases:
  - name: attendance-db
    databaseName: attendance_db
    user: attendance_user

services:
  - type: web
    name: attendance-portal
    env: python
    buildCommand: |
      pip install -r requirements.txt
      python -c "from app import app, db; app.app_context().push(); db.create_all()"
    startCommand: gunicorn -w 4 -b 0.0.0.0:$PORT app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
      - key: SECRET_KEY
        generateValue: true
      - key: FLASK_ENV
        value: production
      - key: DB_HOST
        fromDatabase:
          name: attendance-db
          property: host
      - key: DB_USER
        fromDatabase:
          name: attendance-db
          property: user
      - key: DB_PASSWORD
        fromDatabase:
          name: attendance-db
          property: password
      - key: DB_NAME
        fromDatabase:
          name: attendance-db
          property: database
      - key: TWILIO_ACCOUNT_SID
        sync: false
      - key: TWILIO_AUTH_TOKEN
        sync: false
      - key: TWILIO_WHATSAPP_NUMBER
        sync: false
```

### Step 2: Deploy on Render

1. Go to https://render.com
2. Sign up / Login
3. Click "New +" → "Blueprint"
4. Connect your GitHub repository
5. Select repository with `render.yaml`
6. Click "Apply"
7. Wait for deployment (5-10 minutes)

### Step 3: Configure Environment Variables

1. Go to your service dashboard
2. Environment tab
3. Add Twilio credentials (if using WhatsApp)
4. Save changes

### Step 4: Import Database Schema

```bash
# Get database connection URL from Render
mysql -h your-db-host -u attendance_user -p attendance_db < schema.sql
```

Your app is now live! 🎉

---

## 🐍 PythonAnywhere Deployment

Free tier available for beginners.

### Step 1: Upload Files

1. Sign up at https://www.pythonanywhere.com
2. Go to "Files" tab
3. Upload your project files or clone from Git:
```bash
git clone your-repo-url attendance_portal
```

### Step 2: Setup MySQL Database

1. Go to "Databases" tab
2. Set MySQL password
3. Create database: `attendance_db`
4. Click "Start a console in: attendance_db"
5. Run schema:
```bash
source /home/yourusername/attendance_portal/schema.sql
```

### Step 3: Create Virtual Environment

Open a Bash console:
```bash
cd attendance_portal
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Configure Web App

1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Python 3.10
5. Set Source code: `/home/yourusername/attendance_portal`
6. Set Virtualenv: `/home/yourusername/attendance_portal/venv`

### Step 5: Edit WSGI File

Click on WSGI configuration file link, replace contents:
```python
import sys
import os

# Add your project directory to sys.path
project_home = '/home/yourusername/attendance_portal'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['SECRET_KEY'] = 'your-secret-key'
os.environ['DB_HOST'] = 'yourusername.mysql.pythonanywhere-services.com'
os.environ['DB_USER'] = 'yourusername'
os.environ['DB_PASSWORD'] = 'your-db-password'
os.environ['DB_NAME'] = 'yourusername$attendance_db'
os.environ['FLASK_ENV'] = 'production'

# Import Flask app
from app import app as application
```

### Step 6: Reload and Test

1. Click "Reload" button
2. Visit: `yourusername.pythonanywhere.com`

---

## 🔴 Heroku Deployment

### Step 1: Prepare Files

1. Add `Procfile`:
```
web: gunicorn app:app
```

2. Update `requirements.txt`:
```bash
pip freeze > requirements.txt
```

3. Add `runtime.txt`:
```
python-3.10.12
```

### Step 2: Setup Heroku

```bash
# Install Heroku CLI
# Windows: Download from heroku.com
# Mac: brew install heroku/brew/heroku
# Linux: curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create attendance-portal-app

# Add MySQL addon
heroku addons:create jawsdb:kitefin

# Get database URL
heroku config:get JAWSDB_URL
```

### Step 3: Configure Environment

```bash
# Set environment variables
heroku config:set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
heroku config:set FLASK_ENV=production
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
heroku config:set TWILIO_WHATSAPP_NUMBER=your_number
```

### Step 4: Deploy

```bash
git add .
git commit -m "Prepare for Heroku deployment"
git push heroku main

# Import database
heroku run bash
mysql -h host -u user -p database < schema.sql
exit

# Open app
heroku open
```

---

## ☁️ AWS EC2 Deployment

### Step 1: Launch EC2 Instance

1. Go to AWS Console
2. Launch EC2 instance (Ubuntu 22.04)
3. Choose t2.micro (free tier)
4. Configure security group:
   - SSH (22) - Your IP
   - HTTP (80) - Anywhere
   - HTTPS (443) - Anywhere
   - MySQL (3306) - Same VPC
5. Download key pair

### Step 2: Connect to Instance

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@your-ec2-ip
```

### Step 3: Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and MySQL
sudo apt install python3-pip python3-venv nginx mysql-server -y

# Secure MySQL
sudo mysql_secure_installation
```

### Step 4: Setup Application

```bash
# Clone repository
cd /var/www
sudo git clone your-repo attendance_portal
sudo chown -R ubuntu:ubuntu attendance_portal
cd attendance_portal

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Step 5: Configure Database

```bash
# Import schema
sudo mysql < schema.sql

# Create database user
sudo mysql
CREATE USER 'attendance_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON attendance_db.* TO 'attendance_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 6: Setup Systemd Service

```bash
sudo nano /etc/systemd/system/attendance.service
```

Add:
```ini
[Unit]
Description=Staff Attendance Portal
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/var/www/attendance_portal
Environment="PATH=/var/www/attendance_portal/venv/bin"
Environment="SECRET_KEY=your-secret-key"
Environment="DB_HOST=localhost"
Environment="DB_USER=attendance_user"
Environment="DB_PASSWORD=secure_password"
Environment="DB_NAME=attendance_db"
ExecStart=/var/www/attendance_portal/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

### Step 7: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/attendance
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/attendance /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 8: Start Service

```bash
sudo systemctl start attendance
sudo systemctl enable attendance
sudo systemctl status attendance
```

Your app is now live on EC2! 🎉

---

## 🌊 DigitalOcean Deployment

### Method 1: App Platform (Easiest)

1. Go to DigitalOcean
2. Create → App Platform
3. Connect GitHub repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn -w 4 app:app`
5. Add MySQL database
6. Set environment variables
7. Deploy

### Method 2: Droplet (More Control)

Similar to AWS EC2 instructions above.

1. Create Ubuntu droplet
2. Follow AWS EC2 steps 2-8

---

## 🐳 Docker Deployment

### Step 1: Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### Step 2: Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DB_HOST=db
      - DB_USER=attendance_user
      - DB_PASSWORD=secure_password
      - DB_NAME=attendance_db
      - FLASK_ENV=production
    depends_on:
      - db
    restart: always

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=root_password
      - MYSQL_DATABASE=attendance_db
      - MYSQL_USER=attendance_user
      - MYSQL_PASSWORD=secure_password
    volumes:
      - mysql_data:/var/lib/mysql
      - ./schema.sql:/docker-entrypoint-initdb.d/schema.sql
    restart: always

volumes:
  mysql_data:
```

### Step 3: Deploy

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🔒 Security Checklist

Before going to production:

- [ ] Change default admin password
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS (SSL certificate)
- [ ] Restrict database access
- [ ] Set up firewall rules
- [ ] Use environment variables (never commit .env)
- [ ] Enable database backups
- [ ] Set up monitoring
- [ ] Configure rate limiting
- [ ] Review file permissions

---

## 📊 Post-Deployment

### Monitor Application

```bash
# Check logs
tail -f /var/log/attendance/app.log

# Check service status
sudo systemctl status attendance

# Monitor database
mysql -u root -p
SHOW PROCESSLIST;
```

### Setup Backups

```bash
# Database backup script
#!/bin/bash
mysqldump -u root -p attendance_db > backup_$(date +%Y%m%d).sql

# Add to crontab
crontab -e
0 2 * * * /path/to/backup-script.sh
```

### SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
sudo systemctl reload nginx
```

---

## 🆘 Troubleshooting

### Service won't start
```bash
sudo journalctl -u attendance -n 50
```

### Database connection failed
```bash
mysql -h host -u user -p
# Test connection manually
```

### Port already in use
```bash
sudo lsof -i :5000
sudo kill -9 PID
```

---

**Deployment Complete! 🎉**

Your Staff Attendance Portal is now live and ready to use!




