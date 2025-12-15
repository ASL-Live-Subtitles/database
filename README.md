# Sentiment Analysis DB 

This database schema supports storing user text inputs and corresponding sentiment analysis results. 

---

## `requests` Table

Stores user text input requests submitted for sentiment analysis.

| Column Name | Type | Description |
|--------------|------|-------------|
| **id** | `VARCHAR(36)` | Primary key — unique identifier for each request |
| **input_text** | `TEXT` | The user’s text input to analyze |
| **user_id** | `VARCHAR(36)` | Identifier for the user who made the request |
| **created_at** | `TIMESTAMP` | Timestamp when the request was created |

---

## `sentiments` Table

Stores the sentiment analysis results for each request.

| Column Name | Type | Description |
|--------------|------|-------------|
| **id** | `VARCHAR(36)` | Primary key — unique identifier for each analysis result |
| **request_id** | `VARCHAR(36)` | Foreign key referencing `requests.id` |
| **sentiment** | `VARCHAR(20)` | Sentiment classification (e.g., `positive`, `neutral`, `negative`) |
| **confidence** | `DECIMAL(3,2)` | Confidence score ranging from `0.00` to `1.00` |
| **analyzed_at** | `TIMESTAMP` | Timestamp when the sentiment analysis was performed |

---

# Setup
## Install MySQL 

```bash
gcloud compute ssh mysql-vm --zone=us-central1-a
sudo apt update && sudo apt upgrade -y
sudo apt install -y mysql-server
sudo mysql_secure_installation
```
---

## Configure for Remote Access

#### Edit MySQL configuration
```bash
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
// Update bind-address = 127.0.0.1 to bind-address = 0.0.0.0
sudo systemctl restart mysql
```
#### Configure Firewall
```bash
gcloud compute firewall-rules create allow-mysql-cloud \
    --allow=tcp:3306 \
    --target-tags=mysql-server \
    --source-ranges=10.12.0.15/32 \
    --description="Allow MySQL access for other VMs"
```
---

# Test
<img width="662" height="206" alt="Screenshot 2025-10-18 at 10 28 49 AM" src="https://github.com/user-attachments/assets/162b029b-0221-4b94-b4b8-3a7f92fa3512" />


# Model Serving DB

MySQL schema and helper scripts for storing video-to-gloss inference requests and results used by the model serving service.

---

## Schema

Database: `model_serving_db`  
Table: `video_gloss_requests`

| Column | Type | Notes |
| --- | --- | --- |
| `id` | `VARCHAR(36)` | Primary key for each request |
| `video_uri` | `TEXT` | Optional URI for the uploaded/processed video |
| `landmarks` | `JSON` | Required landmarks payload from the ASL extractor |
| `gloss` | `JSON` | Array of gloss tokens returned by inference |
| `confidence` | `DECIMAL(4,3)` | Overall confidence score |
| `inference_method` | `VARCHAR(32)` | Source of inference (`openai`, `fallback`, etc.) |
| `raw_openai_response` | `JSON` | Optional raw response when using OpenAI |
| `detected` | `BOOLEAN` | Whether the system detected ASL in the video |
| `created_at` | `TIMESTAMP` | Defaults to `CURRENT_TIMESTAMP` |

DDL lives in `const.py` as `VIDEO_GLOSS_REQUESTS_TABLE_SQL`.

---

## Running the helper script

`main.py` drops and recreates the `video_gloss_requests` table in Cloud SQL using the MySQL client.

1) Update connection details and credentials in `const.py` (`CLOUD_SQL_HOST`, `CLOUD_SQL_PORT`, `ROOT_USER`, `ROOT_PASSWORD`, and app user creds if needed).  
2) Uncomment the `create_database` call in `main.py` if the database/user do not exist.  
3) Run:
```bash
cd model_serving_db
python main.py
```
The script drops `video_gloss_requests` (if present) and recreates it. Seed data is available as `VIDEO_GLOSS_TEST_DATA` (commented out in `main.py`).

---

## Manual MySQL invocation (Cloud SQL)

If you prefer issuing SQL yourself:
```bash
mysql -h <CLOUD_SQL_HOST> -P <PORT> -u root -p
-- then run the DDL in const.py
```