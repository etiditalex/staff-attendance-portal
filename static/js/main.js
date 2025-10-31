/**
 * Main JavaScript for Staff Attendance Portal
 * Handles client-side interactions and validations
 */

// ============= Global Variables =============
let confirmationModal;

// ============= Initialization =============
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    initializePopovers();
    initializeFormValidation();
    initializeConfirmations();
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);
});

// ============= Bootstrap Components Initialization =============

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// ============= Form Validation =============

function initializeFormValidation() {
    // Get all forms with needs-validation class
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
    
    // Password confirmation validation
    const confirmPasswordInput = document.getElementById('confirm_password');
    const passwordInput = document.getElementById('password');
    
    if (confirmPasswordInput && passwordInput) {
        confirmPasswordInput.addEventListener('input', function() {
            if (this.value !== passwordInput.value) {
                this.setCustomValidity('Passwords do not match');
            } else {
                this.setCustomValidity('');
            }
        });
        
        passwordInput.addEventListener('input', function() {
            if (confirmPasswordInput.value !== '') {
                if (confirmPasswordInput.value !== this.value) {
                    confirmPasswordInput.setCustomValidity('Passwords do not match');
                } else {
                    confirmPasswordInput.setCustomValidity('');
                }
            }
        });
    }
}

// ============= Confirmation Dialogs =============

function initializeConfirmations() {
    // Add confirmation to logout links
    const logoutLinks = document.querySelectorAll('a[href*="logout"]');
    logoutLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to logout? Your logout time will be recorded.')) {
                e.preventDefault();
            }
        });
    });
}

// ============= Time Display =============

function updateCurrentTime() {
    const timeElements = document.querySelectorAll('.current-time');
    if (timeElements.length > 0) {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        timeElements.forEach(el => {
            el.textContent = timeString;
        });
    }
}

// ============= Table Utilities =============

function filterTable(inputId, tableId) {
    const input = document.getElementById(inputId);
    const filter = input.value.toUpperCase();
    const table = document.getElementById(tableId);
    const tr = table.getElementsByTagName('tr');
    
    for (let i = 1; i < tr.length; i++) {
        let found = false;
        const td = tr[i].getElementsByTagName('td');
        
        for (let j = 0; j < td.length; j++) {
            if (td[j]) {
                const txtValue = td[j].textContent || td[j].innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    found = true;
                    break;
                }
            }
        }
        
        tr[i].style.display = found ? '' : 'none';
    }
}

// ============= Date Utilities =============

function setMinDate(inputId) {
    const dateInput = document.getElementById(inputId);
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
    }
}

function formatDate(date) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(date).toLocaleDateString('en-US', options);
}

function formatTime(time) {
    return new Date(time).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// ============= Notification Utilities =============

function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    
    const icon = getIconForType(type);
    alertDiv.innerHTML = `
        <i class="bi ${icon}"></i> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.classList.remove('show');
            setTimeout(() => alertDiv.remove(), 150);
        }, 5000);
    }
}

function getIconForType(type) {
    const icons = {
        'success': 'bi-check-circle-fill',
        'danger': 'bi-exclamation-triangle-fill',
        'warning': 'bi-exclamation-circle-fill',
        'info': 'bi-info-circle-fill'
    };
    return icons[type] || icons['info'];
}

// ============= Loading Indicator =============

function showLoading(show = true) {
    let loader = document.getElementById('loading-overlay');
    
    if (show && !loader) {
        loader = document.createElement('div');
        loader.id = 'loading-overlay';
        loader.innerHTML = `
            <div class="position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center" 
                 style="background: rgba(0,0,0,0.5); z-index: 9999;">
                <div class="spinner-border text-light" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
        document.body.appendChild(loader);
    } else if (!show && loader) {
        loader.remove();
    }
}

// ============= Export Functions =============

window.filterTable = filterTable;
window.setMinDate = setMinDate;
window.formatDate = formatDate;
window.formatTime = formatTime;
window.showNotification = showNotification;
window.showLoading = showLoading;

// ============= Smooth Scroll =============

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ============= Auto-hide Alerts =============

setTimeout(function() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        const bsAlert = new bootstrap.Alert(alert);
        setTimeout(() => {
            bsAlert.close();
        }, 5000);
    });
}, 100);

// ============= Console Welcome Message =============

console.log('%c Staff Attendance Portal ', 'background: #0d6efd; color: white; font-size: 20px; padding: 10px;');
console.log('%c Built with Flask & Bootstrap ', 'background: #198754; color: white; font-size: 14px; padding: 5px;');




