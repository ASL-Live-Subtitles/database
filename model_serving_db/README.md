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
