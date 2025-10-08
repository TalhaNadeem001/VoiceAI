import axios from 'axios';

// Helper function to convert object to form data
const toFormData = (obj) => {
    const formData = new URLSearchParams();
    for (const key in obj) {
        if (obj.hasOwnProperty(key)) {
            formData.append(key, obj[key]);
        }
    }
    return formData;
};

// Create axios instance with base configuration
const api = axios.create({
    baseURL: '', // Use relative URLs to leverage the proxy
    timeout: 10000,
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        const tokenType = localStorage.getItem('token_type') || 'bearer';
        if (token) {
            config.headers.Authorization = `${tokenType.charAt(0).toUpperCase() + tokenType.slice(1)} ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Token expired or invalid, clear localStorage and redirect to login
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// Auth API calls
export const authAPI = {
    login: (credentials) => api.post('/login', toFormData(credentials)),
    register: (userData) => api.post('/signup', toFormData(userData)),
    logout: () => api.post('/logout'),
    getProfile: () => api.get('/profile'),
};

// Generic API calls
export const apiClient = api;

export default api;
