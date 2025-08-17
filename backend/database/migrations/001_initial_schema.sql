-- Initial schema migration for Enterprise Employee Wellness AI
-- This migration creates all the base tables for the application

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role VARCHAR(50) DEFAULT 'employee',
    department VARCHAR(100),
    position VARCHAR(100),
    manager_id VARCHAR(36),
    company VARCHAR(255),
    phone VARCHAR(20),
    avatar_url VARCHAR(500),
    timezone VARCHAR(50) DEFAULT 'UTC',
    language VARCHAR(10) DEFAULT 'en',
    hire_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    email_verified_at TIMESTAMP,
    last_login TIMESTAMP,
    last_activity TIMESTAMP,
    preferences JSON DEFAULT '{}',
    wellness_profile JSON DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create wellness_entries table
CREATE TABLE IF NOT EXISTS wellness_entries (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    entry_type VARCHAR(50) NOT NULL,
    value FLOAT NOT NULL,
    description TEXT,
    mood_score FLOAT,
    stress_score FLOAT,
    energy_score FLOAT,
    sleep_hours FLOAT,
    sleep_quality FLOAT,
    work_life_balance FLOAT,
    social_support FLOAT,
    physical_activity FLOAT,
    nutrition_quality FLOAT,
    productivity_level FLOAT,
    tags JSON DEFAULT '[]',
    factors JSON DEFAULT '{}',
    recommendations JSON DEFAULT '[]',
    risk_indicators JSON DEFAULT '[]',
    metadata JSON DEFAULT '{}',
    is_anonymous BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    session_id VARCHAR(36) NOT NULL,
    message TEXT NOT NULL,
    sender VARCHAR(20) NOT NULL,
    sentiment VARCHAR(20),
    risk_level VARCHAR(20),
    metadata JSON DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create resources table
CREATE TABLE IF NOT EXISTS resources (
    id VARCHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    difficulty_level VARCHAR(50) NOT NULL,
    duration_minutes INTEGER,
    content_url VARCHAR(500),
    tags JSON DEFAULT '[]',
    author VARCHAR(255),
    rating FLOAT DEFAULT 0.0,
    review_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSON DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create resource_interactions table
CREATE TABLE IF NOT EXISTS resource_interactions (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    resource_id VARCHAR(36) NOT NULL,
    interaction_type VARCHAR(50) NOT NULL,
    rating INTEGER,
    comment TEXT,
    metadata JSON DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (resource_id) REFERENCES resources(id) ON DELETE CASCADE
);

-- Create analytics_events table
CREATE TABLE IF NOT EXISTS analytics_events (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    event_type VARCHAR(100) NOT NULL,
    event_data JSON DEFAULT '{}',
    session_id VARCHAR(36),
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Create risk_assessments table
CREATE TABLE IF NOT EXISTS risk_assessments (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    risk_score FLOAT NOT NULL,
    risk_factors JSON DEFAULT '[]',
    recommendations JSON DEFAULT '[]',
    interventions JSON DEFAULT '[]',
    assessed_by VARCHAR(36),
    status VARCHAR(50) DEFAULT 'active',
    metadata JSON DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assessed_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Create notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    action_url VARCHAR(500),
    metadata JSON DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create team_analytics table
CREATE TABLE IF NOT EXISTS team_analytics (
    id VARCHAR(36) PRIMARY KEY,
    team_id VARCHAR(36) NOT NULL,
    manager_id VARCHAR(36) NOT NULL,
    period_start TIMESTAMP NOT NULL,
    period_end TIMESTAMP NOT NULL,
    metrics JSON DEFAULT '{}',
    insights JSON DEFAULT '[]',
    recommendations JSON DEFAULT '[]',
    risk_alerts JSON DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manager_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create compliance_records table
CREATE TABLE IF NOT EXISTS compliance_records (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    record_type VARCHAR(100) NOT NULL,
    action VARCHAR(100) NOT NULL,
    details JSON DEFAULT '{}',
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Create wellness_goals table
CREATE TABLE IF NOT EXISTS wellness_goals (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    goal_type VARCHAR(100) NOT NULL,
    target_value FLOAT,
    current_value FLOAT,
    unit VARCHAR(50),
    start_date DATE NOT NULL,
    target_date DATE,
    status VARCHAR(50) DEFAULT 'active',
    progress FLOAT DEFAULT 0.0,
    milestones JSON DEFAULT '[]',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create interventions table
CREATE TABLE IF NOT EXISTS interventions (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    intervention_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'scheduled',
    priority VARCHAR(20) DEFAULT 'medium',
    assigned_by VARCHAR(36),
    assigned_to VARCHAR(36),
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    effectiveness_score FLOAT,
    user_feedback TEXT,
    metadata JSON DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_by) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE SET NULL
);

-- Create teams table
CREATE TABLE IF NOT EXISTS teams (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    manager_id VARCHAR(36) NOT NULL,
    department VARCHAR(100),
    team_size INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    wellness_score FLOAT,
    last_assessment TIMESTAMP,
    metadata JSON DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (manager_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create team_members table
CREATE TABLE IF NOT EXISTS team_members (
    id VARCHAR(36) PRIMARY KEY,
    team_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    role VARCHAR(50) DEFAULT 'member',
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create wellness_programs table
CREATE TABLE IF NOT EXISTS wellness_programs (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    program_type VARCHAR(100) NOT NULL,
    target_audience VARCHAR(100),
    start_date DATE NOT NULL,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    max_participants INTEGER,
    current_participants INTEGER DEFAULT 0,
    success_metrics JSON DEFAULT '{}',
    budget FLOAT,
    created_by VARCHAR(36) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE CASCADE
);

-- Create program_participants table
CREATE TABLE IF NOT EXISTS program_participants (
    id VARCHAR(36) PRIMARY KEY,
    program_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    status VARCHAR(50) DEFAULT 'enrolled',
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completion_date TIMESTAMP,
    progress FLOAT DEFAULT 0.0,
    feedback TEXT,
    satisfaction_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES wellness_programs(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create analytics_reports table
CREATE TABLE IF NOT EXISTS analytics_reports (
    id VARCHAR(36) PRIMARY KEY,
    report_type VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    data_period VARCHAR(50) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    metrics JSON DEFAULT '{}',
    insights JSON DEFAULT '[]',
    recommendations JSON DEFAULT '[]',
    generated_by VARCHAR(36),
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (generated_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Create system_settings table
CREATE TABLE IF NOT EXISTS system_settings (
    id VARCHAR(36) PRIMARY KEY,
    setting_key VARCHAR(255) UNIQUE NOT NULL,
    setting_value TEXT NOT NULL,
    setting_type VARCHAR(50) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    is_public BOOLEAN DEFAULT FALSE,
    updated_by VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (updated_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_department ON users(department);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_wellness_entries_user_id ON wellness_entries(user_id);
CREATE INDEX IF NOT EXISTS idx_wellness_entries_created_at ON wellness_entries(created_at);
CREATE INDEX IF NOT EXISTS idx_conversations_user_id ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_session_id ON conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_resources_category ON resources(category);
CREATE INDEX IF NOT EXISTS idx_resources_is_active ON resources(is_active);
CREATE INDEX IF NOT EXISTS idx_resource_interactions_user_id ON resource_interactions(user_id);
CREATE INDEX IF NOT EXISTS idx_resource_interactions_resource_id ON resource_interactions(resource_id);
CREATE INDEX IF NOT EXISTS idx_analytics_events_event_type ON analytics_events(event_type);
CREATE INDEX IF NOT EXISTS idx_risk_assessments_user_id ON risk_assessments(user_id);
CREATE INDEX IF NOT EXISTS idx_risk_assessments_status ON risk_assessments(status);
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
CREATE INDEX IF NOT EXISTS idx_team_analytics_team_id ON team_analytics(team_id);
CREATE INDEX IF NOT EXISTS idx_compliance_records_record_type ON compliance_records(record_type);
CREATE INDEX IF NOT EXISTS idx_wellness_goals_user_id ON wellness_goals(user_id);
CREATE INDEX IF NOT EXISTS idx_interventions_user_id ON interventions(user_id);
CREATE INDEX IF NOT EXISTS idx_teams_manager_id ON teams(manager_id);
CREATE INDEX IF NOT EXISTS idx_team_members_team_id ON team_members(team_id);
CREATE INDEX IF NOT EXISTS idx_team_members_user_id ON team_members(user_id);
CREATE INDEX IF NOT EXISTS idx_wellness_programs_created_by ON wellness_programs(created_by);
CREATE INDEX IF NOT EXISTS idx_program_participants_program_id ON program_participants(program_id);
CREATE INDEX IF NOT EXISTS idx_program_participants_user_id ON program_participants(user_id);
CREATE INDEX IF NOT EXISTS idx_analytics_reports_report_type ON analytics_reports(report_type);
CREATE INDEX IF NOT EXISTS idx_system_settings_setting_key ON system_settings(setting_key);
CREATE INDEX IF NOT EXISTS idx_system_settings_category ON system_settings(category);
