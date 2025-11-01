"""
Email notification service using Flask-Mail
Sends email notifications to managers and directors
"""
from flask_mail import Mail, Message
from datetime import datetime
from models.db import Notification, db

# Global mail instance
mail = None

def init_email_service(app):
    """Initialize Flask-Mail with app configuration"""
    global mail
    
    try:
        mail = Mail(app)
        
        # Check if email is configured
        mail_username = app.config.get('MAIL_USERNAME', '')
        mail_password = app.config.get('MAIL_PASSWORD', '')
        mail_server = app.config.get('MAIL_SERVER', '')
        
        if mail_username and mail_password:
            print(f"✅ Email service initialized successfully")
            print(f"   Server: {mail_server}")
            print(f"   Username: {mail_username}")
            print(f"   Password: {'*' * min(len(mail_password), 10)} (configured)")
        else:
            print("⚠️ Email service not configured. Notifications will be logged but not sent.")
            if not mail_username:
                print("   Missing: MAIL_USERNAME")
            if not mail_password:
                print("   Missing: MAIL_PASSWORD")
    except Exception as e:
        print(f"❌ Failed to initialize email service: {e}")
        import traceback
        traceback.print_exc()
        mail = None
    
    return mail


class EmailService:
    """Service class for sending email notifications"""
    
    def __init__(self, mail_instance):
        """Initialize with Flask-Mail instance"""
        self.mail = mail_instance
    
    def send_email(self, to_email, subject, body, html_body=None):
        """
        Send email to a recipient
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            body (str): Plain text email body
            html_body (str, optional): HTML email body
        
        Returns:
            tuple: (success: bool, message_id or error: str)
        """
        if not self.mail:
            return False, "Email service not configured"
        
        try:
            msg = Message(
                subject=subject,
                recipients=[to_email],
                body=body,
                html=html_body
            )
            
            self.mail.send(msg)
            return True, "Email sent successfully"
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Email send failed: {error_msg}")
            return False, error_msg
    
    def notify_manager_staff_login(self, manager, staff_user, login_time):
        """
        Send notification to manager/director when staff logs in
        
        Args:
            manager: User model instance (manager or director)
            staff_user: User model instance (staff who logged in)
            login_time: datetime object
        
        Returns:
            bool: True if sent successfully
        """
        time_str = login_time.strftime('%I:%M %p')
        date_str = login_time.strftime('%B %d, %Y')
        
        subject = f"Staff Login Notification - {staff_user.name}"
        body = f"""Hello {manager.name},

Staff member {staff_user.name} has logged in to the Attendance Portal.

Details:
- Staff Name: {staff_user.name}
- Email: {staff_user.email}
- Department: {staff_user.department}
- Login Time: {time_str}
- Date: {date_str}

This is an automated notification from the Staff Attendance Portal.

Best regards,
Attendance Portal System
"""
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <h2 style="color: #007bff;">Staff Login Notification</h2>
            <p>Hello {manager.name},</p>
            <p>Staff member <strong>{staff_user.name}</strong> has logged in to the Attendance Portal.</p>
            
            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <h3 style="margin-top: 0;">Details:</h3>
                <ul style="list-style-type: none; padding-left: 0;">
                    <li><strong>Staff Name:</strong> {staff_user.name}</li>
                    <li><strong>Email:</strong> {staff_user.email}</li>
                    <li><strong>Department:</strong> {staff_user.department}</li>
                    <li><strong>Login Time:</strong> {time_str}</li>
                    <li><strong>Date:</strong> {date_str}</li>
                </ul>
            </div>
            
            <p>This is an automated notification from the Staff Attendance Portal.</p>
            <p>Best regards,<br>Attendance Portal System</p>
        </body>
        </html>
        """
        
        # Create notification record (linked to manager)
        notification = Notification(
            user_id=manager.id,
            message=f"Staff {staff_user.name} logged in at {time_str}",
            type='manager_notification'
        )
        db.session.add(notification)
        
        try:
            db.session.commit()
        except:
            db.session.rollback()
        
        # Send email
        success, result = self.send_email(manager.email, subject, body, html_body)
        
        if success:
            notification.mark_sent()
            print(f"✅ Login notification email sent to {manager.name}")
        else:
            notification.mark_failed(result)
            print(f"❌ Failed to send login notification email to {manager.name}: {result}")
        
        return success


# Global email service instance
email_service = None

def get_email_service():
    """Get or create email service instance"""
    global email_service
    if email_service is None and mail:
        email_service = EmailService(mail)
    return email_service

