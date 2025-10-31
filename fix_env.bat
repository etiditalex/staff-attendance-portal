@echo off
echo Fixing .env file for Laragon...
echo.
echo Please check your Laragon MySQL password first:
echo 1. Open Laragon
echo 2. Click Menu - Settings - MySQL
echo 3. Check Root password
echo.
echo Creating .env file...
(
echo # Flask Configuration
echo SECRET_KEY=dev-secret-key-change-in-production-12345
echo FLASK_ENV=development
echo.
echo # Database Configuration - Laragon MySQL
echo # NOTE: If Laragon MySQL has NO password, leave DB_PASSWORD empty
echo # If Laragon MySQL has a password, enter it after the = sign
echo DB_HOST=localhost
echo DB_USER=root
echo DB_PASSWORD=
echo DB_NAME=attendance_db
echo.
echo # Twilio WhatsApp Configuration - Optional
echo TWILIO_ACCOUNT_SID=
echo TWILIO_AUTH_TOKEN=
echo TWILIO_WHATSAPP_NUMBER=
echo.
echo # Application Settings
echo ATTENDANCE_CUTOFF_TIME=09:00
) > .env
echo.
echo .env file created/updated!
echo Please edit it with Notepad and set DB_PASSWORD if Laragon MySQL has a password.
pause



