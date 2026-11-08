-- Schema for TokenWise MVP
-- Table for User/Organization authentication
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    organization_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for API Key Management and Configuration
CREATE TABLE IF NOT EXISTS api_keys (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    key_hash VARCHAR(255) UNIQUE NOT NULL, -- The client's TokenWise Key (Hashed)
    target_llm_vendor VARCHAR(50) NOT NULL DEFAULT 'openai', -- e.g., 'openai', 'gemini'
    client_vendor_key VARCHAR(255) NOT NULL, -- The client's actual LLM key (Encrypted/Hashed)
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Table for Usage Tracking (The core ROI data)
CREATE TABLE IF NOT EXISTS usage_logs (
    id BIGSERIAL PRIMARY KEY,
    api_key_id INTEGER REFERENCES api_keys(id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    t_json INTEGER NOT NULL, -- Theoretical JSON Token Count (Baseline Cost)
    t_actual INTEGER NOT NULL, -- Actual Sent Token Count (Actual Cost)
    conversion_applied BOOLEAN NOT NULL -- Was TOON used?
);

