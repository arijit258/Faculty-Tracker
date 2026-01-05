/**
 * Faculty Tracker - Main JavaScript
 * Easy2Learning Institute
 */

document.addEventListener('DOMContentLoaded', function() {
    // ===== Initialize Components =====
    initSidebar();
    initTooltips();
    initToasts();
    initFormValidation();
    initLoaders();
    initAnimations();
});

/**
 * Sidebar Toggle Functionality
 */
function initSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const toggleBtn = document.getElementById('sidebarToggle');
    
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('open');
            
            // Save state to localStorage
            const isOpen = sidebar.classList.contains('open');
            localStorage.setItem('sidebarOpen', isOpen);
        });
        
        // Restore sidebar state
        const savedState = localStorage.getItem('sidebarOpen');
        if (savedState === 'true') {
            sidebar.classList.add('open');
        }
        
        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', function(e) {
            if (window.innerWidth < 992) {
                if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
                    sidebar.classList.remove('open');
                }
            }
        });
    }
}

/**
 * Initialize Bootstrap Tooltips
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Toast Notifications
 */
function initToasts() {
    // Auto-hide toasts after 3 seconds
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            const bsToast = bootstrap.Toast.getInstance(toast);
            if (bsToast) {
                bsToast.hide();
            }
        }, 3000);
    });
}

/**
 * Form Validation
 */
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}

/**
 * Loading States
 */
function initLoaders() {
    // Add loading state to buttons
    const buttons = document.querySelectorAll('[data-loading]');
    buttons.forEach(btn => {
        btn.addEventListener('click', function() {
            const originalText = this.innerHTML;
            this.setAttribute('data-original-text', originalText);
            this.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
            this.disabled = true;
            
            // Re-enable after 3 seconds (fallback)
            setTimeout(() => {
                this.innerHTML = originalText;
                this.disabled = false;
            }, 3000);
        });
    });
}

/**
 * Scroll Animations
 */
function initAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fadeInUp');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    animatedElements.forEach(el => observer.observe(el));
}

/**
 * Format Time Utility
 */
function formatTime(timeString) {
    const time = new Date('2000-01-01 ' + timeString);
    return time.toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
    });
}

/**
 * Format Date Utility
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

/**
 * Calculate Duration Utility
 */
function calculateDuration(startTime, endTime) {
    const start = new Date('2000-01-01 ' + startTime);
    const end = new Date('2000-01-01 ' + endTime);
    const diffMs = end - start;
    const diffHours = diffMs / (1000 * 60 * 60);
    return Math.round(diffHours * 100) / 100;
}

/**
 * Show Notification
 */
function showNotification(type, message, duration = 3000) {
    const container = document.querySelector('.toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = 'toast show';
    toast.setAttribute('role', 'alert');
    
    let icon = '';
    let title = '';
    
    switch(type) {
        case 'success':
            icon = 'fa-check-circle text-success';
            title = 'Success';
            break;
        case 'error':
            icon = 'fa-exclamation-circle text-danger';
            title = 'Error';
            break;
        case 'warning':
            icon = 'fa-exclamation-triangle text-warning';
            title = 'Warning';
            break;
        case 'info':
            icon = 'fa-info-circle text-info';
            title = 'Info';
            break;
    }
    
    toast.innerHTML = `
        <div class="toast-header">
            <i class="fas ${icon} me-2"></i>
            <strong class="me-auto">${title}</strong>
            <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">${message}</div>
    `;
    
    container.appendChild(toast);
    
    // Initialize toast
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: duration
    });
    bsToast.show();
    
    // Remove from DOM after hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

/**
 * Create Toast Container
 */
function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

/**
 * Confirm Dialog
 */
function confirmDialog(message, onConfirm, onCancel) {
    if (confirm(message)) {
        if (onConfirm) onConfirm();
    } else {
        if (onCancel) onCancel();
    }
}

/**
 * Show Loading Overlay
 */
function showLoading(message = 'Loading...') {
    let overlay = document.querySelector('.loading-overlay');
    
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="text-center">
                <div class="spinner mb-3"></div>
                <p class="text-muted">${message}</p>
            </div>
        `;
        document.body.appendChild(overlay);
    }
    
    overlay.style.display = 'flex';
    return overlay;
}

/**
 * Hide Loading Overlay
 */
function hideLoading() {
    const overlay = document.querySelector('.loading-overlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}

/**
 * Debounce Function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Search Functionality
 */
function initSearch() {
    const searchInput = document.querySelector('.search-box input');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(function(e) {
            const query = e.target.value.trim();
            if (query.length >= 2) {
                // Perform search
                performSearch(query);
            }
        }, 300));
    }
}

/**
 * Perform Search (AJAX)
 */
function performSearch(query) {
    // This would typically make an AJAX call
    console.log('Searching for:', query);
    // Implementation depends on your search endpoint
}

/**
 * Export Data Functions
 */
function exportToPDF(elementId, filename) {
    // This would typically use a library like html2pdf.js
    console.log('Exporting to PDF:', elementId, filename);
}

function exportToExcel(data, filename) {
    // This would typically use a library like SheetJS
    console.log('Exporting to Excel:', data, filename);
}

function exportToCSV(data, filename) {
    // Convert data to CSV and download
    console.log('Exporting to CSV:', data, filename);
}

/**
 * Chart Initialization Helper
 */
function initCharts() {
    // Check if Chart.js is available
    if (typeof Chart !== 'undefined') {
        // Set default options
        Chart.defaults.font.family = "'Inter', sans-serif";
        Chart.defaults.color = '#6b7280';
        Chart.defaults.plugins.legend.position = 'bottom';
        Chart.defaults.plugins.tooltip.backgroundColor = '#1f2937';
        Chart.defaults.plugins.tooltip.padding = 12;
        Chart.defaults.plugins.tooltip.cornerRadius = 8;
    }
}

/**
 * Data Table Functions
 */
function initDataTable(tableId, options = {}) {
    // This would typically use DataTables library
    console.log('Initializing data table:', tableId);
}

function refreshDataTable(tableId) {
    // Refresh data in table
    console.log('Refreshing data table:', tableId);
}

/**
 * AJAX Helper Functions
 */
function ajaxGet(url, options = {}) {
    return fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        }
    })
    .then(response => response.json())
    .catch(error => {
        console.error('AJAX Error:', error);
        showNotification('error', 'An error occurred. Please try again.');
    });
}

function ajaxPost(url, data, options = {}) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
            ...options.headers
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .catch(error => {
        console.error('AJAX Error:', error);
        showNotification('error', 'An error occurred. Please try again.');
    });
}

/**
 * Get CSRF Token
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Date Picker Configuration
 */
function initDatePickers() {
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        // Set max date to today for birth dates
        if (input.id && input.id.includes('date_of_birth')) {
            input.max = new Date().toISOString().split('T')[0];
        }
    });
}

/**
 * Time Picker Configuration
 */
function initTimePickers() {
    const timeInputs = document.querySelectorAll('input[type="time"]');
    timeInputs.forEach(input => {
        input.addEventListener('change', function() {
            validateTimeRange();
        });
    });
}

/**
 * Validate Time Range
 */
function validateTimeRange() {
    const startTime = document.getElementById('id_start_time');
    const endTime = document.getElementById('id_end_time');
    
    if (startTime && endTime) {
        if (startTime.value && endTime.value) {
            if (startTime.value >= endTime.value) {
                endTime.setCustomValidity('End time must be after start time');
            } else {
                endTime.setCustomValidity('');
            }
        }
    }
}

/**
 * Image Preview
 */
function initImagePreviews() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept^="image"]');
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Find or create preview element
                    let preview = input.parentElement.querySelector('.image-preview');
                    if (!preview) {
                        preview = document.createElement('img');
                        preview.className = 'image-preview mt-2 rounded';
                        preview.style.maxWidth = '200px';
                        preview.style.objectFit = 'cover';
                        input.parentElement.appendChild(preview);
                    }
                    preview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    });
}

/**
 * Initialize All Event Listeners
 */
function initEventListeners() {
    // Sidebar toggle
    document.getElementById('sidebarToggle')?.addEventListener('click', function() {
        document.querySelector('.sidebar')?.classList.toggle('open');
    });
    
    // Dropdown hover effect
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('mouseenter', function() {
            this.querySelector('.dropdown-toggle')?.click();
        });
    });
    
    // Card hover effects
    const cards = document.querySelectorAll('.content-card, .stat-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Export functions for use in other scripts
window.FacultyTracker = {
    showNotification,
    showLoading,
    hideLoading,
    confirmDialog,
    formatTime,
    formatDate,
    calculateDuration,
    debounce,
    ajaxGet,
    ajaxPost
};
