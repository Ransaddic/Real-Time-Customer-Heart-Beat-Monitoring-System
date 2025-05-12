-- create "heatbeat_data" table if it does not exist
-- This table will store the heart rate data for each customer
CREATE TABLE IF NOT EXISTS heartbeat_data (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    heart_rate INT NOT NULL,
    CHECK (heart_rate > 0 AND heart_rate < 300)
);

-- create index on timestamp for faster queries
CREATE INDEX IF NOT EXISTS idx_heartbeat_timestamp ON heartbeat_data (timestamp);

