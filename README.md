# 📋 Staff Attendance Web Portal

A complete **Flask-based staff attendance management system** with MySQL database, WhatsApp notifications, and a beautiful Bootstrap UI. This application allows staff to log in/out daily while automatically tracking their attendance, and provides administrators with comprehensive reporting and management tools.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)

---

## ✨ Features

### 👤 Staff Features
- **Easy Sign Up**: Register with name, email, phone, department, and password
- **Automatic Attendance**: Login time recorded automatically when signing in
- **Logout Tracking**: Logout time captured when signing out
- **Personal Dashboard**: View today's attendance and last 7 days history
- **Leave Management**: Request leave or mark remote work days
- **Work Duration**: Automatic calculation of daily work hours
- **WhatsApp Notifications**: Receive login/logout confirmations via WhatsApp
- **Attendance Summary**: View statistics for last 30 days

### 🔐 Admin Features
- **Comprehensive Dashboard**: View all staff attendance in one place
- **Advanced Filtering**: Filter by date, department, or work status
- **Absent Staff Tracking**: See who hasn't logged in
- **CSV Export**: Export attendance data for any date range
- **Real-time Statistics**: Present, absent, remote, and leave counts
- **Manual Editing**: Admin can manually adjust attendance records

### 💬 WhatsApp Integration
- **Login Notifications**: "Hi [Name], you have successfully signed in at [time]"
- **Logout Notifications**: "You have signed out at [time]. Have a good evening!"
- **Work Duration**: Includes hours worked in logout message
- **Powered by Twilio**: Uses Twilio WhatsApp API for reliable delivery

---

## 🗂️ Project Structure

```
attendance_portal/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── schema.sql                  # MySQL database schema
├── env.example                 # Environment variables template
├── README.md                   # This file
│
├── models/
│   └── db.py                   # SQLAlchemy models (User, Attendance, Notification)
│
├── utils/
│   ├── __init__.py
│   └── whatsapp.py            # WhatsApp notification service
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navbar
│   ├── login.html             # Login page
│   ├── signup.html            # Registration page
│   ├── dashboard.html         # Staff dashboard
│   ├── admin.html             # Admin panel
│   ├── 404.html               # 404 error page
│   └── 500.html               # 500 error page
│
└── static/                     # Static assets
    ├── css/
    │   └── style.css          # Custom styles
    └── js/
        └── main.js            # Custom JavaScript
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- Twilio account (for WhatsApp notifications)

### Installation Steps

#### 1. Clone or Download the Project
```bash
cd attendance_portal
```

#### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Setup MySQL Database
```bash
# Login to MySQL
mysql -u root -p

# Run the schema file
source schema.sql

# Or import it
mysql -u root -p < schema.sql
```

#### 5. Configure Environment Variables
```bash
# Copy the example file
cp env.example .env

# Edit .env with your settings
# - Set SECRET_KEY to a random string
# - Configure MySQL credentials
# - Add Twilio credentials for WhatsApp
```

Example `.env` file:
```env
SECRET_KEY=your-super-secret-random-key-here
FLASK_ENV=development

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=attendance_db

TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

ATTENDANCE_CUTOFF_TIME=09:00
```

#### 6. Run the Application
```bash
python app.py
```

The application will be available at: **http://localhost:5000**

#### 7. Default Admin Credentials
- **Email**: `admin@attendance.com`
- **Password**: `admin123`

⚠️ **Important**: Change the admin password immediately after first login!

---

## 🗄️ Database Schema

### Users Table
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| name | VARCHAR(100) | Full name |
| email | VARCHAR(120) | Unique email |
| phone | VARCHAR(20) | Phone number with country code |
| department | VARCHAR(50) | Department name |
| password_hash | VARCHAR(255) | Hashed password |
| role | ENUM | 'staff' or 'admin' |
| status | ENUM | 'active' or 'inactive' |
| created_at | DATETIME | Account creation time |
| updated_at | DATETIME | Last update time |

### Attendance Table
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| user_id | INT | Foreign key to users |
| date | DATE | Attendance date |
| login_time | DATETIME | Login timestamp |
| logout_time | DATETIME | Logout timestamp |
| status | ENUM | 'Present', 'Absent', 'Leave', 'Remote' |
| work_type | ENUM | 'Office', 'Remote', 'Leave' |
| notes | TEXT | Optional notes |
| created_at | DATETIME | Record creation time |
| updated_at | DATETIME | Last update time |

### Notifications Table
| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key |
| user_id | INT | Foreign key to users |
| message | TEXT | Notification content |
| type | ENUM | 'login', 'logout', 'reminder', 'alert' |
| status | ENUM | 'pending', 'sent', 'failed' |
| sent_at | DATETIME | Sent timestamp |
| error_message | TEXT | Error details if failed |
| created_at | DATETIME | Record creation time |

---

## 💬 WhatsApp Setup (Twilio)

### Option 1: Twilio WhatsApp Sandbox (Testing)
1. Create a free Twilio account at https://www.twilio.com/try-twilio
2. Go to Console → Messaging → Try it out → Try WhatsApp
3. Send "join [sandbox-keyword]" to the Twilio WhatsApp number
4. Copy your credentials to `.env`:
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_WHATSAPP_NUMBER` (format: `whatsapp:+14155238886`)

### Option 2: Production WhatsApp Business API
1. Apply for WhatsApp Business API access
2. Get approved by Facebook/Meta
3. Configure your business WhatsApp number
4. Update `.env` with production credentials

### Testing Without WhatsApp
If you don't configure Twilio credentials, the app will work normally but notifications won't be sent. They will be logged in the database with 'failed' status.

---

## 🎨 User Interface

The application features a modern, responsive design built with Bootstrap 5:

- **Mobile-Friendly**: Works perfectly on phones, tablets, and desktops
- **Dark Mode Ready**: Professional color scheme
- **Intuitive Navigation**: Easy-to-use interface for all user levels
- **Real-time Updates**: Auto-dismissing alerts and notifications
- **Smooth Animations**: Pleasant transitions and hover effects

---

## 📊 Usage Guide

### For Staff Members

#### First Time Setup
1. Visit the application URL
2. Click "Sign Up"
3. Fill in your details (name, email, phone, department, password)
4. Submit the form

#### Daily Usage
1. **Morning**: Login to the system → Your login time is automatically recorded
2. **During Day**: View your dashboard to see login time and work duration
3. **Evening**: Logout → Your logout time is automatically recorded
4. **WhatsApp**: Receive notifications on login and logout

#### Requesting Leave
1. Go to Dashboard
2. Click "Request Leave" button
3. Select date and leave type
4. Add optional notes
5. Submit

### For Administrators

#### Viewing Attendance
1. Login with admin credentials
2. View the admin dashboard with all staff attendance
3. Use filters to narrow down by date, department, or status
4. See absent staff in the red alert section

#### Exporting Data
1. Click "Export" button
2. Select date range
3. Download CSV file
4. Open in Excel or Google Sheets

#### Manual Edits
Admins can manually adjust attendance records if needed (feature can be extended in the code).

---

## 🔒 Security Features

- **Password Hashing**: Uses Werkzeug's secure password hashing (PBKDF2)
- **Session Management**: Flask-Login for secure session handling
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **CSRF Protection**: Can be enabled with Flask-WTF
- **Role-Based Access**: Admin vs Staff permissions
- **Environment Variables**: Sensitive data in `.env` file (not in code)

---

## 🚀 Deployment

### Deploy to Render

1. Create a `render.yaml`:
```yaml
services:
  - type: web
    name: attendance-portal
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
      - key: SECRET_KEY
        generateValue: true
      - key: DB_HOST
        fromDatabase:
          name: attendance-db
          property: host
```

2. Add to `requirements.txt`:
```
gunicorn==21.2.0
```

3. Connect your GitHub repository to Render
4. Add environment variables in Render dashboard
5. Deploy!

### Deploy to PythonAnywhere

1. Upload your files to PythonAnywhere
2. Create a MySQL database in the Databases tab
3. Configure a Web app (Flask)
4. Set up virtual environment and install requirements
5. Configure WSGI file:
```python
import sys
path = '/home/yourusername/attendance_portal'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```
6. Reload the web app

### Deploy to VPS (Ubuntu)

```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx mysql-server

# Setup application
cd /var/www
git clone your-repo attendance_portal
cd attendance_portal
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Configure Nginx
sudo nano /etc/nginx/sites-available/attendance

# Configure systemd service
sudo nano /etc/systemd/system/attendance.service

# Start service
sudo systemctl start attendance
sudo systemctl enable attendance
```

---

## 🛠️ Configuration

### Attendance Cutoff Time
Change when staff are marked absent if not logged in:
```env
ATTENDANCE_CUTOFF_TIME=09:00
```

### Session Timeout
Adjust in `config.py`:
```python
PERMANENT_SESSION_LIFETIME = timedelta(hours=12)
```

### Database Connection
For remote MySQL:
```env
DB_HOST=your-mysql-host.com
DB_USER=your_db_user
DB_PASSWORD=your_password
DB_NAME=attendance_db
```

---

## 🧪 Testing

Run the application in development mode:
```bash
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows CMD
$env:FLASK_ENV="development"  # Windows PowerShell

python app.py
```

The app will run with debug mode enabled, showing detailed error messages.

---

## 📝 API Endpoints

While this is a web application, here are the main routes:

| Route | Method | Description | Auth |
|-------|--------|-------------|------|
| `/` | GET | Homepage (redirects) | Public |
| `/signup` | GET, POST | User registration | Public |
| `/login` | GET, POST | User login | Public |
| `/logout` | GET | User logout | Required |
| `/dashboard` | GET | Staff dashboard | Staff |
| `/mark_leave` | POST | Request leave | Staff |
| `/mark_remote` | POST | Mark remote work | Staff |
| `/admin` | GET | Admin panel | Admin |
| `/admin/export_csv` | GET | Export attendance | Admin |
| `/admin/edit_attendance/<id>` | POST | Edit record | Admin |

---

## 🐛 Troubleshooting

### Database Connection Error
```
Error: Access denied for user
```
**Solution**: Check MySQL credentials in `.env` file

### WhatsApp Not Sending
```
WhatsApp service not configured
```
**Solution**: Add Twilio credentials to `.env` or ignore if testing

### Import Error
```
ModuleNotFoundError: No module named 'flask'
```
**Solution**: Activate virtual environment and install requirements

### Port Already in Use
```
Address already in use
```
**Solution**: Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

---

## 🔄 Future Enhancements

- [ ] Biometric integration (fingerprint/face recognition)
- [ ] Mobile app (React Native or Flutter)
- [ ] Geofencing (location-based check-in)
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] Email notifications as backup
- [ ] QR code-based attendance
- [ ] Shift management
- [ ] Overtime tracking
- [ ] Leave approval workflow
- [ ] Integration with HR systems

---

## 📄 License

This project is open source and available for educational and commercial use.

---

## 👥 Support

For issues, questions, or contributions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

## 🙏 Acknowledgments

- **Flask**: Micro web framework
- **Bootstrap**: Frontend framework
- **Twilio**: WhatsApp API
- **MySQL**: Database management
- **SQLAlchemy**: ORM library

---

## 📞 Contact

For deployment support or customization requests, please reach out to your development team.

---

**Built with ❤️ using Flask & Bootstrap**

*Last Updated: 2024*




