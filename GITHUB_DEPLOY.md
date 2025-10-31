# 🚀 GitHub & Render Deployment Guide

Complete step-by-step guide to deploy your Staff Attendance Portal to GitHub and Render.

---

## 📋 Prerequisites

- Git installed on your computer
- GitHub account (free) - https://github.com/signup
- Render account (free) - https://render.com/register
- Your application tested locally

---

## Part 1: Deploy to GitHub

### Step 1: Initialize Git Repository

Open terminal in your project folder:

```bash
# Initialize git repository
git init

# Check status
git status
```

### Step 2: Create .env File (Important!)

Before committing, make sure your `.env` file is NOT tracked:

```bash
# The .gitignore file already excludes .env
# Verify it's ignored:
cat .gitignore | grep .env
```

### Step 3: Stage and Commit Files

```bash
# Add all files
git add .

# Check what will be committed
git status

# Commit with message
git commit -m "Initial commit: Staff Attendance Portal"
```

### Step 4: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `staff-attendance-portal` (or your choice)
3. Description: "Flask-based Staff Attendance Management System with WhatsApp notifications"
4. Choose: **Public** or **Private**
5. DO NOT initialize with README (we already have one)
6. Click "Create repository"

### Step 5: Push to GitHub

GitHub will show you commands. Use these:

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/staff-attendance-portal.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Enter your GitHub credentials when prompted.**

### Step 6: Verify on GitHub

1. Refresh your GitHub repository page
2. You should see all your files
3. ✅ Verify `.env` is NOT visible (good!)

---

## Part 2: Deploy to Render

### Step 1: Sign Up for Render

1. Go to https://render.com/register
2. Sign up with GitHub (recommended)
3. Authorize Render to access your repositories

### Step 2: Create MySQL Database

1. In Render dashboard, click **"New +"**
2. Select **"PostgreSQL"** or use external MySQL
   - **Option A**: Use external MySQL (like PlanetScale - free tier)
   - **Option B**: Use Render's PostgreSQL (modify code slightly)

**For MySQL (Recommended):**
- Sign up for free MySQL at: https://planetscale.com or https://www.freemysqlhosting.net
- Get connection details

### Step 3: Deploy Web Service

1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository:
   - Click "Configure account" if needed
   - Select `staff-attendance-portal` repository
3. Configure the service:
   - **Name**: `staff-attendance-portal`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     gunicorn -w 4 -b 0.0.0.0:$PORT app:app
     ```
   - **Plan**: Free

### Step 4: Add Environment Variables

Scroll to **"Environment Variables"** section and add:

```
SECRET_KEY = (click "Generate" for random value)
FLASK_ENV = production
DB_HOST = your_mysql_host
DB_USER = your_mysql_user
DB_PASSWORD = your_mysql_password
DB_NAME = attendance_db
TWILIO_ACCOUNT_SID = (optional - leave blank for now)
TWILIO_AUTH_TOKEN = (optional - leave blank for now)
TWILIO_WHATSAPP_NUMBER = (optional - leave blank for now)
ATTENDANCE_CUTOFF_TIME = 09:00
```

### Step 5: Create Service

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Watch the logs for any errors

### Step 6: Initialize Database

Once deployed, you need to create the database tables:

**Option A: Using Render Shell**
1. Go to your service dashboard
2. Click "Shell" tab
3. Run:
```bash
python init_db.py
```

**Option B: Using MySQL Client**
1. Connect to your MySQL database
2. Run the `schema.sql` file:
```bash
mysql -h your_host -u your_user -p your_database < schema.sql
```

### Step 7: Test Your Deployment

1. Render will show you a URL like: `https://staff-attendance-portal.onrender.com`
2. Click on it to open your application
3. Try logging in with:
   - Email: `admin@attendance.com`
   - Password: `admin123`
4. ✅ **Change the admin password immediately!**

---

## Part 3: Post-Deployment Setup

### 1. Change Admin Password

1. Login to admin account
2. Go to profile (you may need to add this feature, or use database)
3. Change password from `admin123` to something secure

### 2. Configure WhatsApp (Optional)

1. Sign up for Twilio: https://www.twilio.com/try-twilio
2. Get WhatsApp sandbox credentials
3. Update environment variables in Render:
   - Go to service → Environment
   - Add Twilio credentials
   - Click "Save Changes"
4. Service will automatically redeploy

### 3. Add Custom Domain (Optional)

1. In Render dashboard, go to Settings → Custom Domain
2. Add your domain
3. Update DNS records as instructed
4. SSL certificate will be auto-generated

---

## 📊 Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] MySQL database created and configured
- [ ] Web service deployed on Render
- [ ] Environment variables added
- [ ] Database initialized (tables created)
- [ ] Application accessible via URL
- [ ] Admin login tested
- [ ] Admin password changed
- [ ] WhatsApp configured (optional)
- [ ] Test staff signup and attendance

---

## 🔄 Making Updates

### Update Your Code

```bash
# Make changes to your code
# Then commit and push

git add .
git commit -m "Description of changes"
git push origin main

# Render will automatically detect and redeploy!
```

---

## 🐛 Troubleshooting

### Build Failed

**Check Render logs:**
1. Go to service dashboard
2. Click "Logs" tab
3. Look for error messages

**Common issues:**
- Missing dependencies in `requirements.txt`
- Python version mismatch
- Syntax errors in code

### Database Connection Error

**Check:**
1. Environment variables are correct
2. Database host is accessible from Render
3. MySQL credentials are valid
4. Database name exists

**Test connection:**
```bash
# In Render Shell
python -c "from app import db; print(db)"
```

### Application Not Loading

**Check:**
1. Render logs for errors
2. Environment variables set correctly
3. Database initialized
4. Start command is correct

### WhatsApp Not Working

**Solutions:**
- Verify Twilio credentials
- Check phone number format: `+1234567890`
- Join Twilio WhatsApp sandbox
- Check Twilio account status
- **App works without WhatsApp**, so not critical

---

## 💰 Cost Breakdown

### Free Tier Usage

**GitHub:**
- ✅ Unlimited public repositories
- ✅ Unlimited private repos (with limits)
- ✅ Free forever

**Render (Free Tier):**
- ✅ 750 hours/month (enough for 24/7)
- ✅ Automatic SSL
- ✅ Automatic deploys from GitHub
- ⚠️ **Sleeps after 15 min inactivity** (wakes on visit)
- ⚠️ Limited to 512 MB RAM

**MySQL Options:**
- PlanetScale: Free tier with 5 GB storage
- FreeMySQLHosting: Free with limitations
- Clever Cloud: Free tier available

### Upgrade for Production

For real production use (no sleep, more resources):
- Render Starter: $7/month
- Database: $7-15/month
- Total: ~$15-25/month

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** ✅ (already in .gitignore)
2. **Change default passwords** immediately
3. **Use strong SECRET_KEY** (auto-generated in Render)
4. **Enable HTTPS** (automatic in Render)
5. **Restrict database access** (allow only Render IP)
6. **Regular backups** (export database weekly)
7. **Monitor logs** (check for suspicious activity)

---

## 📱 Mobile Access

Your app is mobile-responsive! Staff can:
1. Open on any phone browser
2. Add to home screen (works like an app)
3. Mark attendance from anywhere

---

## 🎉 Success!

Your Staff Attendance Portal is now live on the internet!

**Share your URL with your team:**
`https://your-app-name.onrender.com`

**Next Steps:**
1. Have staff members sign up
2. Test the attendance flow
3. Monitor the admin dashboard
4. Export reports as needed

---

## 📞 Need Help?

**Render Support:**
- Documentation: https://render.com/docs
- Community: https://community.render.com

**GitHub Help:**
- Documentation: https://docs.github.com
- Community: https://github.community

**Project Issues:**
- Create issue in your GitHub repository
- Check logs for error messages
- Review environment variables

---

**Congratulations on deploying your application! 🚀**



