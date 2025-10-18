# Database Schema 

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
