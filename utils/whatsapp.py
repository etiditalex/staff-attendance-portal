"""
WhatsApp notification service using Twilio API
Sends attendance notifications to staff members
"""
from twilio.rest import Client
from datetime import datetime
import os
from models.db import Notification, db

class WhatsAppService:
    """Service class for sending WhatsApp messages via Twilio"""
    
    def __init__(self, account_sid, auth_token, whatsapp_number):
        """Initialize Twilio client"""
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.whatsapp_number = whatsapp_number
        self.client = None
        
        # Initialize client if credentials are provided
        if account_sid and auth_token:
            try:
                self.client = Client(account_sid, auth_token)
            except Exception as e:
                print(f"⚠️ Failed to initialize Twilio client: {e}")
    
    def send_message(self, to_phone, message):
        """
        Send WhatsApp message to a phone number
        
        Args:
            to_phone (str): Recipient phone number (format: +1234567890)
            message (str): Message content
        
        Returns:
            tuple: (success: bool, message_sid or error: str)
        """
        if not self.client:
            return False, "WhatsApp service not configured"
        
        try:
            # Ensure phone number has whatsapp: prefix
            if not to_phone.startswith('whatsapp:'):
                to_phone = f'whatsapp:{to_phone}'
            
            # Send message
            message_obj = self.client.messages.create(
                body=message,
                from_=self.whatsapp_number,
                to=to_phone
            )
            
            return True, message_obj.sid
        
        except Exception as e:
            error_msg = str(e)
            print(f"❌ WhatsApp send failed: {error_msg}")
            return False, error_msg
    
    def send_login_notification(self, user, login_time):
        """
        Send login notification to user
        
        Args:
            user: User model instance
            login_time: datetime object
        """
        time_str = login_time.strftime('%I:%M %p')
        message = f"Hi {user.name},\n\nYou have successfully signed in at {time_str}.\n\nHave a productive day! 🚀"
        
        # Create notification record
        notification = Notification(
            user_id=user.id,
            message=message,
            type='login'
        )
        db.session.add(notification)
        db.session.commit()
        
        # Send WhatsApp message
        success, result = self.send_message(user.phone, message)
        
        if success:
            notification.mark_sent()
            print(f"✅ Login notification sent to {user.name}")
        else:
            notification.mark_failed(result)
            print(f"❌ Failed to send login notification to {user.name}")
        
        return success
    
    def send_logout_notification(self, user, logout_time, work_duration=None):
        """
        Send logout notification to user
        
        Args:
            user: User model instance
            logout_time: datetime object
            work_duration: float (hours worked)
        """
        time_str = logout_time.strftime('%I:%M %p')
        message = f"Hi {user.name},\n\nYou have signed out at {time_str}."
        
        if work_duration:
            message += f"\n\nToday's work duration: {work_duration} hours."
        
        message += "\n\nHave a good evening! 🌙"
        
        # Create notification record
        notification = Notification(
            user_id=user.id,
            message=message,
            type='logout'
        )
        db.session.add(notification)
        db.session.commit()
        
        # Send WhatsApp message
        success, result = self.send_message(user.phone, message)
        
        if success:
            notification.mark_sent()
            print(f"✅ Logout notification sent to {user.name}")
        else:
            notification.mark_failed(result)
            print(f"❌ Failed to send logout notification to {user.name}")
        
        return success
    
    def send_reminder(self, user, message):
        """
        Send custom reminder to user
        
        Args:
            user: User model instance
            message: str (custom message)
        """
        # Create notification record
        notification = Notification(
            user_id=user.id,
            message=message,
            type='reminder'
        )
        db.session.add(notification)
        db.session.commit()
        
        # Send WhatsApp message
        success, result = self.send_message(user.phone, message)
        
        if success:
            notification.mark_sent()
        else:
            notification.mark_failed(result)
        
        return success
    
    def notify_manager_staff_login(self, manager, staff_user, login_time):
        """
        Send WhatsApp notification to manager/director when staff logs in
        
        Args:
            manager: User model instance (manager or director)
            staff_user: User model instance (staff who logged in)
            login_time: datetime object
        
        Returns:
            bool: True if sent successfully
        """
        time_str = login_time.strftime('%I:%M %p')
        date_str = login_time.strftime('%B %d, %Y')
        
        message = f"""🔔 Staff Login Notification

Hello {manager.name},

Staff member {staff_user.name} has logged in to the Attendance Portal.

📋 Details:
• Name: {staff_user.name}
• Email: {staff_user.email}
• Department: {staff_user.department}
• Login Time: {time_str}
• Date: {date_str}

This is an automated notification from the Attendance Portal."""
        
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
        
        # Send WhatsApp message
        success, result = self.send_message(manager.phone, message)
        
        if success:
            notification.mark_sent()
            print(f"✅ Login notification WhatsApp sent to manager {manager.name}")
        else:
            notification.mark_failed(result)
            print(f"❌ Failed to send login notification WhatsApp to manager {manager.name}: {result}")
        
        return success


# Global WhatsApp service instance
whatsapp_service = None

def init_whatsapp_service(app):
    """Initialize WhatsApp service with app configuration"""
    global whatsapp_service
    
    account_sid = app.config.get('TWILIO_ACCOUNT_SID')
    auth_token = app.config.get('TWILIO_AUTH_TOKEN')
    whatsapp_number = app.config.get('TWILIO_WHATSAPP_NUMBER')
    
    whatsapp_service = WhatsAppService(account_sid, auth_token, whatsapp_number)
    
    if whatsapp_service.client:
        print("✅ WhatsApp service initialized successfully")
    else:
        print("⚠️ WhatsApp service not configured. Notifications will be logged but not sent.")
    
    return whatsapp_service




