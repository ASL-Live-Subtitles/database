# === Admin ===


CLOUD_SQL_HOST = "136.113.187.126"   # from SQL instance details page
CLOUD_SQL_PORT = 3306


ROOT_USER = "root"
ROOT_PASSWORD = "modelservingpassword"  # If you set a root password during hardening, put it here (or leave None)

# === App DB/user ===
ASL_DB_NAME = "model_serving_db"
ASL_DB_USER = "model_serving_user"
ASL_DB_PASSWORD = "H7!qZ9p#L2vBn3" 

# === Table names (to keep usage consistent) ===
USERS_TABLE_NAME = "users"
MODELS_TABLE_NAME = "models"
SESSIONS_TABLE_NAME = "sessions"
GESTURES_TABLE_NAME = "gestures"
PREDICTIONS_TABLE_NAME = "predictions"
CAPTIONS_TABLE_NAME = "captions"

# === DDL (MySQL 8.0) ===

USERS_TABLE_SQL = f"""
CREATE TABLE {USERS_TABLE_NAME} (
    user_id      VARCHAR(64) PRIMARY KEY,
    display_name VARCHAR(100),
    created_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

MODELS_TABLE_SQL = f"""
CREATE TABLE {MODELS_TABLE_NAME} (
    model_id      BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name          VARCHAR(128) NOT NULL,
    version       VARCHAR(32)  NOT NULL,
    model_type    ENUM('tensorflow','pytorch','onnx','other') NOT NULL,
    artifact_uri  VARCHAR(512) NOT NULL,
    input_shape   JSON NOT NULL,
    output_shape  JSON NOT NULL,
    status        ENUM('active','inactive','deprecated') NOT NULL DEFAULT 'active',
    metrics       JSON NULL,
    sha256        CHAR(64) NULL,
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uq_model_name_version (name, version),
    KEY idx_models_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

SESSIONS_TABLE_SQL = f"""
CREATE TABLE {SESSIONS_TABLE_NAME} (
    session_id   BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    user_id      VARCHAR(64) NULL,
    device_label VARCHAR(64) NULL,
    started_at   TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ended_at     TIMESTAMP NULL,
    KEY idx_sessions_user_time (user_id, started_at),
    CONSTRAINT fk_sessions_user FOREIGN KEY (user_id) REFERENCES {USERS_TABLE_NAME}(user_id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

GESTURES_TABLE_SQL = f"""
CREATE TABLE {GESTURES_TABLE_NAME} (
    gesture_id         BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    session_id         BIGINT UNSIGNED NULL,
    user_id            VARCHAR(64) NULL,
    landmarks          JSON NOT NULL,
    frame_width        INT NULL,
    frame_height       INT NULL,
    source             ENUM('web','mobile','other') DEFAULT 'web',
    received_at        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    model_id           BIGINT UNSIGNED NULL,
    predicted_label    VARCHAR(64) NULL,
    confidence         DECIMAL(6,5) NULL CHECK (confidence >= 0.0 AND confidence <= 1.0),
    probs              JSON NULL,
    processing_time_ms INT NULL,
    processed_at       TIMESTAMP NULL,

    KEY idx_g_user_time (user_id, received_at),
    KEY idx_g_session_time (session_id, received_at),
    KEY idx_g_model (model_id),
    CONSTRAINT fk_g_session FOREIGN KEY (session_id) REFERENCES {SESSIONS_TABLE_NAME}(session_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_g_user FOREIGN KEY (user_id) REFERENCES {USERS_TABLE_NAME}(user_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_g_model FOREIGN KEY (model_id) REFERENCES {MODELS_TABLE_NAME}(model_id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

PREDICTIONS_TABLE_SQL = f"""
CREATE TABLE {PREDICTIONS_TABLE_NAME} (
    prediction_id      BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    requestor_user_id  VARCHAR(64) NULL,
    session_id         BIGINT UNSIGNED NULL,
    model_id           BIGINT UNSIGNED NULL,

    status             ENUM('queued','running','succeeded','failed','canceled') NOT NULL DEFAULT 'queued',
    created_at         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started_at         TIMESTAMP NULL,
    completed_at       TIMESTAMP NULL,

    params             JSON NULL,
    output_text        TEXT NULL,
    confidence         DECIMAL(6,5) NULL CHECK (confidence >= 0.0 AND confidence <= 1.0),
    latency_ms         INT NULL,
    error_message      TEXT NULL,

    KEY idx_pred_status (status, created_at),
    KEY idx_pred_session (session_id, created_at),
    KEY idx_pred_model (model_id),

    CONSTRAINT fk_p_user FOREIGN KEY (requestor_user_id) REFERENCES {USERS_TABLE_NAME}(user_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_p_session FOREIGN KEY (session_id) REFERENCES {SESSIONS_TABLE_NAME}(session_id)
        ON DELETE SET NULL ON UPDATE CASCADE,
    CONSTRAINT fk_p_model FOREIGN KEY (model_id) REFERENCES {MODELS_TABLE_NAME}(model_id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

CAPTIONS_TABLE_SQL = f"""
CREATE TABLE {CAPTIONS_TABLE_NAME} (
    caption_id    BIGINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    session_id    BIGINT UNSIGNED NOT NULL,
    prediction_id BIGINT UNSIGNED NULL,
    start_ms      INT NOT NULL,
    end_ms        INT NOT NULL,
    text          TEXT NOT NULL,
    source        ENUM('lm','heuristic','manual') DEFAULT 'lm',
    confidence    DECIMAL(6,5) NULL CHECK (confidence >= 0.0 AND confidence <= 1.0),

    KEY idx_captions_session_time (session_id, start_ms),
    CONSTRAINT fk_c_session FOREIGN KEY (session_id) REFERENCES {SESSIONS_TABLE_NAME}(session_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT fk_c_prediction FOREIGN KEY (prediction_id) REFERENCES {PREDICTIONS_TABLE_NAME}(prediction_id)
        ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

# === Optional seed data (same pattern as their sample inserts) ===
USERS_TEST_DATA = f"""
INSERT INTO {USERS_TABLE_NAME} (user_id, display_name) VALUES
('test_user_123', 'Test User')
ON DUPLICATE KEY UPDATE display_name=VALUES(display_name);
"""

MODELS_TEST_DATA = f"""
INSERT INTO {MODELS_TABLE_NAME}
(name, version, model_type, artifact_uri, input_shape, output_shape, status, metrics)
VALUES
('ASL_Letter_Classifier', '1.0.0', 'tensorflow', '/models/asl_letters.h5',
 JSON_ARRAY(21,2), JSON_ARRAY(26), 'active', JSON_OBJECT('top1_acc',0.962,'f1',0.934));
"""

GESTURES_TEST_DATA = f"""
INSERT INTO {GESTURES_TABLE_NAME} (user_id, landmarks)
VALUES
('test_user_123', JSON_ARRAY(JSON_ARRAY(0.1,0.2), JSON_ARRAY(0.3,0.4), JSON_ARRAY(0.5,0.6)));
"""
