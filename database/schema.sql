-- Speech Synthesize MySQL 8.x schema
-- UTF-8 English text storage and synthesis job history.

CREATE DATABASE IF NOT EXISTS speech_synthesize
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE speech_synthesize;

CREATE TABLE IF NOT EXISTS voices (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    backend VARCHAR(64) NOT NULL DEFAULT 'pyttsx3',
    voice_id VARCHAR(512) NOT NULL,
    name VARCHAR(255) NOT NULL,
    language VARCHAR(32) NOT NULL DEFAULT 'en-US',
    gender VARCHAR(32) NULL,
    enabled BOOLEAN NOT NULL DEFAULT TRUE,
    metadata JSON NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_voice_backend_id (backend, voice_id),
    KEY idx_voice_language (language),
    KEY idx_voice_enabled (enabled)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS synthesis_jobs (
    id CHAR(36) NOT NULL,
    backend VARCHAR(64) NOT NULL DEFAULT 'pyttsx3',
    text_content LONGTEXT NOT NULL,
    language VARCHAR(32) NOT NULL DEFAULT 'en-US',
    voice_id VARCHAR(512) NULL,
    rate SMALLINT UNSIGNED NOT NULL DEFAULT 180,
    volume DECIMAL(4,3) NOT NULL DEFAULT 1.000,
    output_format VARCHAR(16) NOT NULL DEFAULT 'wav',
    output_path VARCHAR(1024) NULL,
    status ENUM('queued','running','completed','failed') NOT NULL DEFAULT 'queued',
    error_message TEXT NULL,
    duration_seconds DECIMAL(12,3) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    PRIMARY KEY (id),
    KEY idx_jobs_status_created (status, created_at),
    KEY idx_jobs_voice (voice_id),
    KEY idx_jobs_language (language)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS application_settings (
    setting_key VARCHAR(128) NOT NULL,
    setting_value TEXT NOT NULL,
    setting_type ENUM('string','integer','decimal','boolean','json') NOT NULL DEFAULT 'string',
    description VARCHAR(512) NULL,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (setting_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO application_settings (setting_key, setting_value, setting_type, description)
VALUES
 ('default_language', 'en-US', 'string', 'Default English speech locale'),
 ('default_rate', '180', 'integer', 'Default speech rate'),
 ('default_volume', '1.0', 'decimal', 'Default speech volume'),
 ('default_backend', 'pyttsx3', 'string', 'Default local speech backend'),
 ('max_text_characters', '100000', 'integer', 'Maximum synthesis input size')
ON DUPLICATE KEY UPDATE setting_value = VALUES(setting_value), description = VALUES(description);

CREATE OR REPLACE VIEW english_synthesis_jobs AS
SELECT id, backend, voice_id, rate, volume, output_format, output_path,
       status, duration_seconds, created_at, started_at, completed_at
FROM synthesis_jobs
WHERE language LIKE 'en%';
