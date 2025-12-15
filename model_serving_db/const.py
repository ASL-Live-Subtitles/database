# === Admin ===

CLOUD_SQL_HOST = "136.113.187.126"   # from SQL instance details page (or use proxy/socket)
CLOUD_SQL_PORT = 3306

ROOT_USER = "root"
ROOT_PASSWORD = "modelservingpassword"  # If you set a root password during hardening, put it here (or leave None)

# === App DB/user ===
ASL_DB_NAME = "model_serving_db"
ASL_DB_USER = "model_serving_user"
ASL_DB_PASSWORD = "H7!qZ9p#L2vBn3"

# === Table name ===
VIDEO_GLOSS_REQUESTS_TABLE = "video_gloss_requests"

# === DDL (single-table schema) ===
VIDEO_GLOSS_REQUESTS_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {VIDEO_GLOSS_REQUESTS_TABLE} (
    id VARCHAR(36) PRIMARY KEY,
    video_uri TEXT NULL,
    landmarks JSON NOT NULL,
    gloss JSON NOT NULL,              -- array of gloss tokens, e.g., ["HELLO"]
    confidence DECIMAL(4,3) NOT NULL,
    inference_method VARCHAR(32) NOT NULL, -- openai | fallback
    raw_openai_response JSON NULL,
    detected BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

# Optional seed data (empty by default)
VIDEO_GLOSS_TEST_DATA = f"""
INSERT INTO {VIDEO_GLOSS_REQUESTS_TABLE} (id, video_uri, landmarks, gloss, confidence, inference_method, detected)
VALUES
('demo-req-001', 'gs://bucket/sample.mp4', JSON_ARRAY(JSON_ARRAY(0.5,0.6)), JSON_ARRAY('HELLO'), 0.9, 'stub', TRUE)
ON DUPLICATE KEY UPDATE gloss=VALUES(gloss);
"""
