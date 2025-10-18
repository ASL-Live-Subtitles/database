ROOT_USER = "root"
ROOT_PASSWORD = None 

SENTIMENT_DB_NAME = "sentiment_detection"
SENTIMENT_DB_USER = "sentiment_user"
SENTIMENT_DB_PASSWORD = "sentiment_password123"

REQUESTS_TABLE_NAME = "requests"
SENTIMENTS_TABLE_NAME = "sentiments"

REQUESTS_TABLE_SQL = """
CREATE TABLE requests (
    id VARCHAR(36) PRIMARY KEY,
    input_text TEXT NOT NULL,
    user_id VARCHAR(36),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

SENTIMENTS_TABLE_SQL = """
CREATE TABLE sentiments (
    id VARCHAR(36) PRIMARY KEY,
    request_id VARCHAR(36) NOT NULL,
    sentiment VARCHAR(20) NOT NULL,
    confidence DECIMAL(3,2) NOT NULL CHECK (confidence >= 0.0 AND confidence <= 1.0),
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES requests(id) ON DELETE CASCADE
);
"""

REQUESTS_TEST_DATA = """
INSERT INTO requests (id, input_text, user_id) VALUES
('req-001', 'I love this product! It is amazing.', 'user-123'),
('req-002', 'It is okay, nothing special.', 'user-789'),
('req-003', 'Absolutely fantastic experience!', 'user-123');
"""

SENTIMENTS_TEST_DATA = """
INSERT INTO sentiments (id, request_id, sentiment, confidence) VALUES
('sent-001', 'req-001', 'positive', 0.95),
('sent-002', 'req-002', 'neutral', 0.76),
('sent-003', 'req-003', 'positive', 0.92);
"""
