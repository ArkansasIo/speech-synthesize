-- English defaults for speech_synthesize.
USE speech_synthesize;

INSERT INTO application_settings (setting_key, setting_value, setting_type, description)
VALUES
 ('default_language', 'en-US', 'string', 'English United States locale'),
 ('english_locale', 'en_US', 'string', 'English locale identifier'),
 ('english_encoding', 'utf-8', 'string', 'Text encoding for English input'),
 ('default_rate', '180', 'integer', 'Default English speech rate'),
 ('default_volume', '1.0', 'decimal', 'Default English speech volume'),
 ('default_backend', 'pyttsx3', 'string', 'Local speech backend'),
 ('max_text_characters', '100000', 'integer', 'Maximum synthesis input length')
ON DUPLICATE KEY UPDATE
 setting_value = VALUES(setting_value),
 setting_type = VALUES(setting_type),
 description = VALUES(description);
