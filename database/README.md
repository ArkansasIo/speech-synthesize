# MySQL Database

The Speech Synthesize database uses MySQL 8.x and `utf8mb4` for full Unicode storage while defaulting the application speech locale to English (`en-US`).

## Create the database

Run `database/schema.sql` with a MySQL 8.x client:

```bash
mysql -u root -p < database/schema.sql
```

## Application user

Create a least-privilege application account separately from the schema file:

```sql
CREATE USER 'speech_app'@'localhost' IDENTIFIED BY 'CHANGE_THIS_PASSWORD';
GRANT SELECT, INSERT, UPDATE, DELETE ON speech_synthesize.* TO 'speech_app'@'localhost';
FLUSH PRIVILEGES;
```

Use an environment variable for the password:

```bash
# Linux/macOS
export SPEECH_DB_PASSWORD='CHANGE_THIS_PASSWORD'

# PowerShell
$env:SPEECH_DB_PASSWORD = 'CHANGE_THIS_PASSWORD'
```

Do not commit real credentials to Git.

## English library configuration

`config/mysql.toml` defines:

- MySQL connection parameters
- `utf8mb4` character encoding
- `en-US` as the default speech locale
- English locale `en_US`
- `pyttsx3` as the default local TTS backend
- 180 words/minute default rate
- 1.0 default volume

The database stores voice metadata and synthesis-job history; actual audio files remain in the configured output directory rather than inside MySQL.
