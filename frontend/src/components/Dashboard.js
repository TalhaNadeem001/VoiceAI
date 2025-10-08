import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const Dashboard = () => {
    const { user } = useAuth();

    return (
        <div className="dashboard-minimal">
            <div className="dashboard-container">
                {/* Header */}
                <header className="dashboard-header">
                    <h1>VoiceAI Dashboard</h1>
                    <p>Manage your voice AI assistant</p>
                </header>

                {/* Main Content */}
                <main className="dashboard-main">
                    {/* Content hidden - showing only header */}
                </main>
            </div>
        </div>
    );
};

export default Dashboard;
