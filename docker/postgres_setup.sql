-- Create heartbeat_data table if it does not exist
CREATE TABLE IF NOT EXISTS heartbeat_data (
    id SERIAL PRIMARY KEY,
    customer_id UUID NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    heart_rate INT NOT NULL,
    CHECK (heart_rate > 0 AND heart_rate < 300)
);

-- Indexes for optimized querying
CREATE INDEX IF NOT EXISTS idx_heartbeat_timestamp ON heartbeat_data (timestamp);
CREATE INDEX IF NOT EXISTS idx_heartbeat_customer_id ON heartbeat_data (customer_id);
