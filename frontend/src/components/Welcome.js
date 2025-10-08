import React from 'react';
import { Link } from 'react-router-dom';

const Welcome = () => {
    return (
        <div className="welcome-minimal">
            <div className="welcome-container">
                {/* Header */}
                <header className="welcome-header">
                    <div className="logo">
                        <h1>VoiceAI</h1>
                    </div>
                    <nav className="welcome-nav">
                        <Link to="/login" className="nav-link">Login</Link>
                        <Link to="/register" className="nav-link nav-button">Sign Up</Link>
                    </nav>
                </header>

                {/* Main Content */}
                <main className="welcome-main">
                    <div className="hero-section">
                        <h2 className="hero-title">
                            AI Voice Agent for Your Business
                        </h2>
                        <p className="hero-description">
                            Let our intelligent voice agent handle calls, book appointments,
                            and provide 24/7 customer service.
                        </p>
                        <div className="hero-actions">
                            <Link to="/register" className="btn-primary">
                                Get Started
                            </Link>
                            <Link to="/login" className="btn-secondary">
                                Sign In
                            </Link>
                        </div>
                    </div>

                    {/* Simple Features */}
                    <section className="features-section">
                        <div className="feature">
                            <h3>📞 Always Available</h3>
                            <p>Never miss a call. AI answers 24/7.</p>
                        </div>
                        <div className="feature">
                            <h3>📅 Smart Booking</h3>
                            <p>Automatically schedule appointments.</p>
                        </div>
                        <div className="feature">
                            <h3>🤖 Natural Conversations</h3>
                            <p>Human-like AI interactions.</p>
                        </div>
                    </section>
                </main>

                {/* Simple Footer */}
                <footer className="welcome-footer">
                    <p>&copy; 2024 VoiceAI. All rights reserved.</p>
                </footer>
            </div>
        </div>
    );
};

export default Welcome;
