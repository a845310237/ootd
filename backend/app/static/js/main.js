/**
 * Main JavaScript file for OOTD application
 * Handles common utilities and API interactions
 */

// API base URL
const API_BASE = '/api/v1';

// Get authentication token from localStorage
function getAuthToken() {
    return localStorage.getItem('access_token');
}

// Set authentication token
function setAuthToken(token) {
    localStorage.setItem('access_token', token);
}

// Clear authentication token
function clearAuthToken() {
    localStorage.removeItem('access_token');
}

// Check if user is authenticated
function isAuthenticated() {
    return !!getAuthToken();
}

// Redirect if not authenticated
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = '/auth/login';
    }
}

// Logout function
function logout() {
    clearAuthToken();
    window.location.href = '/auth/login';
}

// API helper function
async function apiCall(endpoint, options = {}) {
    const token = getAuthToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers,
    });

    if (response.status === 401) {
        // Token expired or invalid
        clearAuthToken();
        window.location.href = '/auth/login';
        throw new Error('未授权');
    }

    return response;
}

// Debounce utility function
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

// Format date utility
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    });
}

// Format date time utility
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
}

// Show alert with timeout
function showAlert(message, type = 'info', duration = 3000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `fixed top-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 ${
        type === 'error' ? 'bg-red-500 text-white' :
        type === 'success' ? 'bg-green-500 text-white' :
        'bg-blue-500 text-white'
    }`;
    alertDiv.textContent = message;
    document.body.appendChild(alertDiv);

    setTimeout(() => {
        alertDiv.remove();
    }, duration);
}

// Show loading overlay
function showLoading() {
    const overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
    overlay.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(overlay);
}

// Hide loading overlay
function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.remove();
    }
}

// Modal management
const Modal = {
    show(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('hidden');
            modal.classList.add('flex');
        }
    },

    hide(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }
    },

    toggle(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            if (modal.classList.contains('hidden')) {
                this.show(modalId);
            } else {
                this.hide(modalId);
            }
        }
    },
};

// Image preview utility
function previewImage(input, previewId) {
    const preview = document.getElementById(previewId);
    const file = input.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
}

// File upload utility
async function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiCall('/upload', {
        method: 'POST',
        headers: {}, // Let browser set Content-Type for FormData
        body: formData,
    });

    if (!response.ok) {
        throw new Error('文件上传失败');
    }

    return await response.json();
}

// Pagination utility
function paginate(items, page, perPage) {
    const start = (page - 1) * perPage;
    const end = start + perPage;
    return {
        items: items.slice(start, end),
        totalPages: Math.ceil(items.length / perPage),
        currentPage: page,
    };
}

// Search utility
function searchItems(items, searchTerm, searchFields) {
    if (!searchTerm) return items;

    const term = searchTerm.toLowerCase();
    return items.filter(item =>
        searchFields.some(field => {
            const value = item[field];
            return value && value.toString().toLowerCase().includes(term);
        })
    );
}

// Filter utility
function filterItems(items, filters) {
    return items.filter(item => {
        return Object.entries(filters).every(([key, value]) => {
            if (!value) return true;
            return item[key] === value;
        });
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Check authentication for protected pages
    const protectedPaths = ['/dashboard'];
    const currentPath = window.location.pathname;

    if (protectedPaths.some(path => currentPath.startsWith(path))) {
        requireAuth();
    }

    // Add click event listeners to all close-modal buttons
    document.querySelectorAll('.close-modal').forEach(button => {
        button.addEventListener('click', function() {
            const modal = this.closest('[id$="Modal"]');
            if (modal) {
                modal.classList.add('hidden');
                modal.classList.remove('flex');
            }
        });
    });

    // Close modals when clicking outside
    document.querySelectorAll('[id$="Modal"]').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.add('hidden');
                this.classList.remove('flex');
            }
        });
    });
});

// Export utilities for use in other scripts
window.OOTDUtils = {
    apiCall,
    debounce,
    formatDate,
    formatDateTime,
    showAlert,
    showLoading,
    hideLoading,
    Modal,
    previewImage,
    uploadFile,
    paginate,
    searchItems,
    filterItems,
    getAuthToken,
    setAuthToken,
    clearAuthToken,
    isAuthenticated,
    logout,
};
