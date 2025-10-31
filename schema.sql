-- ===============================================
-- Staff Attendance Portal - Database Schema
-- MySQL Database Schema
-- ===============================================

-- Create database
CREATE DATABASE IF NOT EXISTS attendance_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE attendance_db;

-- ===============================================
-- Table: users
-- Stores staff and admin user information
-- ===============================================

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    department VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('staff', 'admin') DEFAULT 'staff' NOT NULL,
    status ENUM('active', 'inactive') DEFAULT 'active' NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_department (department),
    INDEX idx_role (role),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ===============================================
-- Table: attendance
-- Stores daily attendance records
-- ===============================================

CREATE TABLE IF NOT EXISTS attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    login_time DATETIME NULL,
    logout_time DATETIME NULL,
    status ENUM('Present', 'Absent', 'Leave', 'Remote') DEFAULT 'Absent' NOT NULL,
    work_type ENUM('Office', 'Remote', 'Leave') DEFAULT 'Office' NOT NULL,
    notes TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_date (user_id, date),
    INDEX idx_user_id (user_id),
    INDEX idx_date (date),
    INDEX idx_status (status),
    INDEX idx_user_date (user_id, date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ===============================================
-- Table: notifications
-- Stores WhatsApp notification logs
-- ===============================================

CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    type ENUM('login', 'logout', 'reminder', 'alert') NOT NULL,
    status ENUM('pending', 'sent', 'failed') DEFAULT 'pending' NOT NULL,
    sent_at DATETIME NULL,
    error_message TEXT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_type (type),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ===============================================
-- Insert Default Admin User
-- Email: admin@attendance.com
-- Password: admin123
-- ===============================================

INSERT INTO users (name, email, phone, department, password_hash, role, status) 
VALUES (
    'Admin User',
    'admin@attendance.com',
    '+1234567890',
    'Administration',
    'pbkdf2:sha256:600000$YourHashedPasswordHere',  -- This will be replaced by app initialization
    'admin',
    'active'
) ON DUPLICATE KEY UPDATE email = email;

-- ===============================================
-- Sample Data (Optional - for testing)
-- ===============================================

-- Sample Staff Users
INSERT INTO users (name, email, phone, department, password_hash, role, status) VALUES
('John Doe', 'john.doe@company.com', '+1234567891', 'Engineering', 'pbkdf2:sha256:600000$hash', 'staff', 'active'),
('Jane Smith', 'jane.smith@company.com', '+1234567892', 'Sales', 'pbkdf2:sha256:600000$hash', 'staff', 'active'),
('Mike Johnson', 'mike.johnson@company.com', '+1234567893', 'Marketing', 'pbkdf2:sha256:600000$hash', 'staff', 'active'),
('Sarah Williams', 'sarah.williams@company.com', '+1234567894', 'Human Resources', 'pbkdf2:sha256:600000$hash', 'staff', 'active'),
('David Brown', 'david.brown@company.com', '+1234567895', 'Finance', 'pbkdf2:sha256:600000$hash', 'staff', 'active')
ON DUPLICATE KEY UPDATE email = email;

-- ===============================================
-- Useful Queries for Maintenance
-- ===============================================

-- Get today's attendance summary
-- SELECT 
--     status,
--     COUNT(*) as count
-- FROM attendance
-- WHERE date = CURDATE()
-- GROUP BY status;

-- Get users who haven't logged in today
-- SELECT u.id, u.name, u.email, u.department
-- FROM users u
-- LEFT JOIN attendance a ON u.id = a.user_id AND a.date = CURDATE()
-- WHERE u.role = 'staff' AND u.status = 'active' AND a.id IS NULL;

-- Get attendance report for a specific date range
-- SELECT 
--     u.name,
--     u.department,
--     a.date,
--     a.login_time,
--     a.logout_time,
--     a.status,
--     a.work_type,
--     TIMESTAMPDIFF(HOUR, a.login_time, a.logout_time) as hours_worked
-- FROM attendance a
-- JOIN users u ON a.user_id = u.id
-- WHERE a.date BETWEEN '2024-01-01' AND '2024-12-31'
-- ORDER BY a.date DESC, u.name;

-- Get notification statistics
-- SELECT 
--     type,
--     status,
--     COUNT(*) as count
-- FROM notifications
-- GROUP BY type, status;

-- ===============================================
-- Indexes for Performance Optimization
-- ===============================================

-- Composite indexes for common queries
CREATE INDEX idx_attendance_date_status ON attendance(date, status);
CREATE INDEX idx_attendance_user_date_desc ON attendance(user_id, date DESC);
CREATE INDEX idx_notifications_user_created ON notifications(user_id, created_at DESC);

-- ===============================================
-- Views for Common Queries
-- ===============================================

-- View: Today's Attendance Summary
CREATE OR REPLACE VIEW v_today_attendance AS
SELECT 
    u.id as user_id,
    u.name,
    u.email,
    u.department,
    a.login_time,
    a.logout_time,
    a.status,
    a.work_type,
    CASE 
        WHEN a.login_time IS NOT NULL AND a.logout_time IS NOT NULL 
        THEN TIMESTAMPDIFF(MINUTE, a.login_time, a.logout_time) / 60.0
        ELSE NULL
    END as hours_worked
FROM users u
LEFT JOIN attendance a ON u.id = a.user_id AND a.date = CURDATE()
WHERE u.role = 'staff' AND u.status = 'active'
ORDER BY u.name;

-- View: Monthly Attendance Statistics
CREATE OR REPLACE VIEW v_monthly_stats AS
SELECT 
    u.id as user_id,
    u.name,
    u.department,
    DATE_FORMAT(a.date, '%Y-%m') as month,
    SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) as present_days,
    SUM(CASE WHEN a.status = 'Remote' THEN 1 ELSE 0 END) as remote_days,
    SUM(CASE WHEN a.status = 'Leave' THEN 1 ELSE 0 END) as leave_days,
    SUM(CASE WHEN a.status = 'Absent' THEN 1 ELSE 0 END) as absent_days,
    COUNT(*) as total_days
FROM users u
JOIN attendance a ON u.id = a.user_id
WHERE u.role = 'staff' AND u.status = 'active'
GROUP BY u.id, u.name, u.department, DATE_FORMAT(a.date, '%Y-%m')
ORDER BY month DESC, u.name;

-- ===============================================
-- Triggers for Audit Trail
-- ===============================================

-- Trigger to log user changes
DELIMITER //

CREATE TRIGGER before_user_update
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END//

CREATE TRIGGER before_attendance_update
BEFORE UPDATE ON attendance
FOR EACH ROW
BEGIN
    SET NEW.updated_at = CURRENT_TIMESTAMP;
END//

DELIMITER ;

-- ===============================================
-- Stored Procedures
-- ===============================================

DELIMITER //

-- Procedure to get user attendance summary
CREATE PROCEDURE sp_user_attendance_summary(IN p_user_id INT, IN p_days INT)
BEGIN
    SELECT 
        date,
        login_time,
        logout_time,
        status,
        work_type,
        CASE 
            WHEN login_time IS NOT NULL AND logout_time IS NOT NULL 
            THEN TIMESTAMPDIFF(MINUTE, login_time, logout_time) / 60.0
            ELSE NULL
        END as hours_worked
    FROM attendance
    WHERE user_id = p_user_id
        AND date >= DATE_SUB(CURDATE(), INTERVAL p_days DAY)
    ORDER BY date DESC;
END//

-- Procedure to mark absent users
CREATE PROCEDURE sp_mark_absent_users(IN p_date DATE)
BEGIN
    -- Insert absent records for users who haven't logged in
    INSERT INTO attendance (user_id, date, status, work_type)
    SELECT 
        u.id,
        p_date,
        'Absent',
        'Office'
    FROM users u
    WHERE u.role = 'staff' 
        AND u.status = 'active'
        AND NOT EXISTS (
            SELECT 1 
            FROM attendance a 
            WHERE a.user_id = u.id AND a.date = p_date
        );
END//

DELIMITER ;

-- ===============================================
-- Grant Permissions (adjust as needed)
-- ===============================================

-- CREATE USER IF NOT EXISTS 'attendance_user'@'localhost' IDENTIFIED BY 'your_secure_password';
-- GRANT SELECT, INSERT, UPDATE, DELETE ON attendance_db.* TO 'attendance_user'@'localhost';
-- FLUSH PRIVILEGES;

-- ===============================================
-- Database Backup Recommendation
-- ===============================================

-- Run this command to backup the database:
-- mysqldump -u root -p attendance_db > attendance_backup_$(date +%Y%m%d).sql

-- To restore:
-- mysql -u root -p attendance_db < attendance_backup_YYYYMMDD.sql




