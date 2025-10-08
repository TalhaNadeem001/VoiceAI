import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../services/api';

const AuthContext = createContext();

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);

    // Check if user is logged in on app start
    useEffect(() => {
        const token = localStorage.getItem('token');
        const tokenType = localStorage.getItem('token_type');
        const savedUser = localStorage.getItem('user');

        if (token && tokenType && savedUser) {
            try {
                const userData = JSON.parse(savedUser);
                setUser(userData);
                setIsAuthenticated(true);
                setLoading(false);
            } catch (error) {
                logout();
                setLoading(false);
            }
        } else {
            setLoading(false);
        }
    }, []);

    const login = async (credentials) => {
        try {
            setLoading(true);
            const response = await authAPI.login(credentials);
            console.log('Login response:', response.data); // Debug log
            console.log('Available fields:', Object.keys(response.data)); // Debug log to see all fields

            const { access_token, token_type, first_name, last_name, email } = response.data;

            // Store the access token and user data
            if (access_token && token_type) {
                localStorage.setItem('token', access_token);
                localStorage.setItem('token_type', token_type);

                // Create user object with data from login response
                const userData = {
                    first_name: first_name || 'User',
                    last_name: last_name || '',
                    email: email || '',
                    id: 'user'
                };

                console.log('User data being stored:', userData); // Debug log
                localStorage.setItem('user', JSON.stringify(userData));
                setUser(userData);
                setIsAuthenticated(true);
            } else {
                throw new Error('No access token received from server');
            }

            return { success: true };
        } catch (error) {
            let message = 'Login failed';

            console.log('Login error:', error.response?.data); // Debug log

            if (error.response?.data) {
                const errorData = error.response.data;

                // Handle different error response formats
                if (typeof errorData === 'string') {
                    message = errorData;
                } else if (errorData.detail) {
                    message = errorData.detail;
                } else if (errorData.message) {
                    message = errorData.message;
                } else if (Array.isArray(errorData) && errorData.length > 0) {
                    // Handle validation errors array
                    message = errorData[0].msg || errorData[0].message || 'Validation error';
                } else if (errorData.msg) {
                    message = errorData.msg;
                } else {
                    message = 'Login failed';
                }
            }

            return { success: false, error: message };
        } finally {
            setLoading(false);
        }
    };

    const register = async (userData) => {
        try {
            setLoading(true);
            const response = await authAPI.register(userData);
            const { token, user: newUser } = response.data;

            localStorage.setItem('token', token);
            localStorage.setItem('user', JSON.stringify(newUser));

            setUser(newUser);
            setIsAuthenticated(true);

            return { success: true };
        } catch (error) {
            let message = 'Registration failed';

            if (error.response?.data) {
                const errorData = error.response.data;

                // Handle different error response formats
                if (typeof errorData === 'string') {
                    message = errorData;
                } else if (errorData.detail) {
                    message = errorData.detail;
                } else if (errorData.message) {
                    message = errorData.message;
                } else if (Array.isArray(errorData) && errorData.length > 0) {
                    // Handle validation errors array
                    message = errorData[0].msg || errorData[0].message || 'Validation error';
                } else if (errorData.msg) {
                    message = errorData.msg;
                } else {
                    message = 'Registration failed';
                }
            }

            return { success: false, error: message };
        } finally {
            setLoading(false);
        }
    };

    const logout = async () => {
        try {
            await authAPI.logout();
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            localStorage.removeItem('token');
            localStorage.removeItem('token_type');
            localStorage.removeItem('user');
            setUser(null);
            setIsAuthenticated(false);
        }
    };

    const value = {
        user,
        isAuthenticated,
        loading,
        login,
        register,
        logout,
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};
