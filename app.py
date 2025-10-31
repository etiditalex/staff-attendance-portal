"""
Staff Attendance Portal - Main Application
Flask web application for managing staff attendance with WhatsApp notifications
"""
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
from datetime import datetime, date, timedelta
from sqlalchemy import and_, or_, func, text
from sqlalchemy.exc import OperationalError
import csv
import io

# Local imports
from config import config
from models.db import db, User, Attendance, Notification, init_db
from utils.whatsapp import init_whatsapp_service, whatsapp_service

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = 'development'  # Change to 'production' when deploying
app.config.from_object(config[env])

# Initialize database (with auto-table creation)
init_db(app)

# Force database initialization on startup
with app.app_context():
    try:
        # Ensure all tables exist
        db.create_all()
        print("✅ Database tables checked/created on startup")
        
        # Create admin user if doesn't exist
        admin = User.query.filter_by(email='admin@attendance.com').first()
        if not admin:
            admin = User(
                name='Admin User',
                email='admin@attendance.com',
                phone='+1234567890',
                department='Administration',
                role='admin',
                status='active'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created on startup")
    except Exception as e:
        print(f"⚠️ Database initialization warning: {e}")
        # Continue anyway - tables will be created on first request

# Initialize WhatsApp service
init_whatsapp_service(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


# ============= CONNECTION ERROR HANDLING =============

@app.before_request
def before_request():
    """Ensure database connection before each request"""
    # Remove connection test - let SQLAlchemy handle it automatically
    # The pool_pre_ping will handle connection checks
    pass


# ============= DECORATORS =============

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You need admin privileges to access this page.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


# ============= AUTHENTICATION ROUTES =============

@app.route('/')
def index():
    """Homepage - redirect based on login status"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        department = request.form.get('department', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validation
        if not all([name, email, phone, department, password]):
            flash('All fields are required.', 'danger')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('signup.html')
        
        # Check if user already exists
        try:
            existing_user = User.query.filter_by(email=email).first()
        except OperationalError:
            db.session.rollback()
            existing_user = User.query.filter_by(email=email).first()
        
        if existing_user:
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('login'))
        
        # Create new user
        try:
            # Ensure tables exist before creating user
            try:
                db.create_all()
            except:
                pass  # Tables might already exist
            
            new_user = User(
                name=name,
                email=email,
                phone=phone,
                department=department,
                role='staff',
                status='active'
            )
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        
        except Exception as e:
            db.session.rollback()
            # Log the error for debugging
            print(f"❌ Signup error: {str(e)}")
            import traceback
            traceback.print_exc()
            flash(f'Error creating account: {str(e)}', 'danger')
            return render_template('signup.html')
    
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page with automatic attendance marking"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not email or not password:
            flash('Please provide both email and password.', 'danger')
            return render_template('login.html')
        
        # Find user (with error handling for lost connections)
        try:
            user = User.query.filter_by(email=email).first()
        except OperationalError:
            db.session.rollback()
            try:
                user = User.query.filter_by(email=email).first()
            except:
                flash('Database connection error. Please try again.', 'danger')
                return render_template('login.html')
        
        if not user or not user.check_password(password):
            flash('Invalid email or password.', 'danger')
            return render_template('login.html')
        
        if user.status != 'active':
            flash('Your account is inactive. Please contact admin.', 'warning')
            return render_template('login.html')
        
        # Log user in
        login_user(user, remember=remember)
        
        # Mark attendance (only for staff, not admin)
        if not user.is_admin():
            try:
                today = date.today()
                attendance = Attendance.query.filter_by(user_id=user.id, date=today).first()
                
                if not attendance:
                    # Create new attendance record
                    attendance = Attendance(
                        user_id=user.id,
                        date=today,
                        status='Present',
                        work_type='Office'
                    )
                    db.session.add(attendance)
                
                # Mark login time
                if not attendance.login_time:
                    attendance.mark_login()
                    
                    # Send WhatsApp notification
                    try:
                        whatsapp_service.send_login_notification(user, attendance.login_time)
                    except Exception as e:
                        print(f"WhatsApp notification error: {e}")
            except OperationalError:
                db.session.rollback()
        
        flash(f'Welcome back, {user.name}!', 'success')
        
        # Redirect to next page or dashboard
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('dashboard'))
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """User logout with automatic attendance marking"""
    # Mark logout time if not admin
    if not current_user.is_admin():
        try:
            today = date.today()
            attendance = Attendance.query.filter_by(user_id=current_user.id, date=today).first()
            
            if attendance and not attendance.logout_time:
                attendance.mark_logout()
                work_duration = attendance.get_work_duration()
                
                # Send WhatsApp notification
                try:
                    whatsapp_service.send_logout_notification(current_user, attendance.logout_time, work_duration)
                except Exception as e:
                    print(f"WhatsApp notification error: {e}")
        except OperationalError:
            db.session.rollback()
    
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))


# ============= USER DASHBOARD =============

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing today's attendance and recent history"""
    if current_user.is_admin():
        return redirect(url_for('admin_panel'))
    
    try:
        # Get today's attendance
        today = date.today()
        today_attendance = current_user.get_today_attendance()
        
        # Get last 7 days attendance
        start_date = today - timedelta(days=6)
        recent_attendance = Attendance.query.filter(
            Attendance.user_id == current_user.id,
            Attendance.date >= start_date
        ).order_by(Attendance.date.desc()).all()
        
        # Get summary statistics
        summary = current_user.get_attendance_summary(30)  # Last 30 days
        
        return render_template('dashboard.html',
                             user=current_user,
                             today_attendance=today_attendance,
                             recent_attendance=recent_attendance,
                             summary=summary,
                             today=today)
    except OperationalError:
        db.session.rollback()
        flash('Database connection error. Please refresh.', 'warning')
        return render_template('dashboard.html',
                             user=current_user,
                             today_attendance=None,
                             recent_attendance=[],
                             summary={},
                             today=date.today())


@app.route('/mark_leave', methods=['POST'])
@login_required
def mark_leave():
    """Mark leave for a specific date"""
    if current_user.is_admin():
        flash('Admin users cannot mark leave.', 'warning')
        return redirect(url_for('admin_panel'))
    
    leave_date_str = request.form.get('leave_date')
    leave_type = request.form.get('leave_type', 'Leave')
    notes = request.form.get('notes', '')
    
    try:
        leave_date = datetime.strptime(leave_date_str, '%Y-%m-%d').date()
        
        # Check if date is not in the past (except today)
        if leave_date < date.today():
            flash('Cannot mark leave for past dates.', 'danger')
            return redirect(url_for('dashboard'))
        
        # Check if attendance already exists
        attendance = Attendance.query.filter_by(user_id=current_user.id, date=leave_date).first()
        
        if attendance:
            # Update existing record
            attendance.status = leave_type
            attendance.work_type = leave_type
            attendance.notes = notes
        else:
            # Create new record
            attendance = Attendance(
                user_id=current_user.id,
                date=leave_date,
                status=leave_type,
                work_type=leave_type,
                notes=notes
            )
            db.session.add(attendance)
        
        db.session.commit()
        flash(f'{leave_type} marked successfully for {leave_date.strftime("%B %d, %Y")}.', 'success')
    
    except ValueError:
        flash('Invalid date format.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'Error marking leave: {str(e)}', 'danger')
    
    return redirect(url_for('dashboard'))


@app.route('/mark_remote', methods=['POST'])
@login_required
def mark_remote():
    """Mark remote work for today"""
    if current_user.is_admin():
        flash('Admin users cannot mark remote work.', 'warning')
        return redirect(url_for('admin_panel'))
    
    today = date.today()
    try:
        attendance = current_user.get_today_attendance()
        
        if attendance:
            attendance.work_type = 'Remote'
            attendance.status = 'Remote'
            db.session.commit()
            flash('Marked as working remotely today.', 'success')
        else:
            flash('Please login first to mark remote work.', 'warning')
    except OperationalError:
        db.session.rollback()
        flash('Database error. Please try again.', 'danger')
    
    return redirect(url_for('dashboard'))


# ============= ADMIN PANEL =============

@app.route('/admin')
@login_required
@admin_required
def admin_panel():
    """Admin panel for viewing all attendance records"""
    try:
        # Get filter parameters
        filter_date = request.args.get('date', date.today().strftime('%Y-%m-%d'))
        filter_department = request.args.get('department', 'all')
        filter_status = request.args.get('status', 'all')
        
        try:
            target_date = datetime.strptime(filter_date, '%Y-%m-%d').date()
        except:
            target_date = date.today()
        
        # Base query
        query = db.session.query(Attendance, User).join(User).filter(Attendance.date == target_date)
        
        # Apply filters
        if filter_department != 'all':
            query = query.filter(User.department == filter_department)
        
        if filter_status != 'all':
            query = query.filter(Attendance.status == filter_status)
        
        # Get results
        attendance_records = query.order_by(User.name).all()
        
        # Get list of departments
        departments = db.session.query(User.department).distinct().all()
        departments = [d[0] for d in departments]
        
        # Get absent users for the selected date
        absent_users = Attendance.get_absent_users(target_date)
        
        # Statistics
        total_staff = User.query.filter_by(role='staff', status='active').count()
        present_count = Attendance.query.filter_by(date=target_date, status='Present').count()
        remote_count = Attendance.query.filter_by(date=target_date, status='Remote').count()
        leave_count = Attendance.query.filter_by(date=target_date, status='Leave').count()
        absent_count = len(absent_users)
        
        stats = {
            'total': total_staff,
            'present': present_count,
            'remote': remote_count,
            'leave': leave_count,
            'absent': absent_count
        }
        
        return render_template('admin.html',
                             attendance_records=attendance_records,
                             departments=departments,
                             filter_date=filter_date,
                             filter_department=filter_department,
                             filter_status=filter_status,
                             absent_users=absent_users,
                             stats=stats)
    except OperationalError:
        db.session.rollback()
        flash('Database connection error. Please refresh.', 'warning')
        return render_template('admin.html',
                             attendance_records=[],
                             departments=[],
                             filter_date=date.today().strftime('%Y-%m-%d'),
                             filter_department='all',
                             filter_status='all',
                             absent_users=[],
                             stats={'total': 0, 'present': 0, 'remote': 0, 'leave': 0, 'absent': 0})


@app.route('/admin/export_csv')
@login_required
@admin_required
def export_csv():
    """Export attendance data to CSV"""
    # Get filter parameters
    start_date_str = request.args.get('start_date', (date.today() - timedelta(days=30)).strftime('%Y-%m-%d'))
    end_date_str = request.args.get('end_date', date.today().strftime('%Y-%m-%d'))
    
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except:
        start_date = date.today() - timedelta(days=30)
        end_date = date.today()
    
    try:
        # Query attendance records
        records = db.session.query(Attendance, User).join(User).filter(
            and_(Attendance.date >= start_date, Attendance.date <= end_date)
        ).order_by(Attendance.date.desc(), User.name).all()
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Date', 'Name', 'Email', 'Department', 'Login Time', 'Logout Time', 
                        'Status', 'Work Type', 'Duration (hrs)', 'Notes'])
        
        # Write data
        for attendance, user in records:
            writer.writerow([
                attendance.date.strftime('%Y-%m-%d'),
                user.name,
                user.email,
                user.department,
                attendance.format_time(attendance.login_time),
                attendance.format_time(attendance.logout_time),
                attendance.status,
                attendance.work_type,
                attendance.get_work_duration() or 'N/A',
                attendance.notes or ''
            ])
        
        # Prepare response
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'attendance_{start_date}_{end_date}.csv'
        )
    except OperationalError:
        db.session.rollback()
        flash('Database error during export.', 'danger')
        return redirect(url_for('admin_panel'))


@app.route('/admin/edit_attendance/<int:attendance_id>', methods=['POST'])
@login_required
@admin_required
def edit_attendance(attendance_id):
    """Admin can manually edit attendance records"""
    try:
        attendance = Attendance.query.get_or_404(attendance_id)
        
        status = request.form.get('status')
        work_type = request.form.get('work_type')
        notes = request.form.get('notes', '')
        
        if status:
            attendance.status = status
        if work_type:
            attendance.work_type = work_type
        
        attendance.notes = notes
        
        db.session.commit()
        flash('Attendance record updated successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating record: {str(e)}', 'danger')
    
    return redirect(url_for('admin_panel'))


# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('500.html'), 500


# ============= CONTEXT PROCESSORS =============

@app.context_processor
def utility_processor():
    """Add utility functions to template context"""
    def format_date(dt):
        if isinstance(dt, date):
            return dt.strftime('%B %d, %Y')
        return 'N/A'
    
    def format_time(dt):
        if isinstance(dt, datetime):
            return dt.strftime('%I:%M %p')
        return 'N/A'
    
    return dict(format_date=format_date, format_time=format_time)


# ============= MAIN =============

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("🚀 Starting Staff Attendance Portal")
    print("=" * 60)
    print("\n📊 Application starting at: http://localhost:5000")
    print("📧 Default admin: admin@attendance.com / admin123")
    print("\n💡 Press CTRL+C to stop the server\n")
    print("=" * 60 + "\n")
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
