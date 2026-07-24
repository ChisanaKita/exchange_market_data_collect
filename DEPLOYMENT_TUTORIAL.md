# 🚀 AWS EC2 Deployment & Operation Tutorial

This tutorial provides complete, step-by-step instructions for deploying and running the **Unified Crypto Market Data Collector** on an AWS EC2 instance.

---

## 📋 Prerequisites & Planning

### 1. Recommended EC2 Instance
* **Instance Type**: `c6g.medium` (AWS Graviton ARM64 processor). Highly recommended because it offers dedicated core scheduling (no throttling during peak market hours) and is cheaper than Intel equivalents.
* **Alternative**: `t4g.small` (~$12/month) for budget deployments.
* **Storage**: 30GB - 50GB EBS GP3 volume.
* **OS**: Ubuntu 22.04 LTS or Amazon Linux 2023.

### 2. IAM Role for S3 Access (Security Best Practice)
Instead of putting AWS root or secret keys in `.env` files, attach an IAM Role to your EC2 instance. Create a policy with the following restricted permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowCollectorS3Operations",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:PutObjectAcl",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::your-market-data-bucket",
                "arn:aws:s3:::your-market-data-bucket/crypto-market-data/*"
            ]
        }
    ]
}
```

---

## 🛠️ Step-by-Step Deployment Guide

### Step 1: Copy Codebase to EC2
If you haven't already, copy your folder (excluding any `.venv` or temporary caches) to your EC2 directory:
```bash
# Example if using scp from your local machine:
# scp -r -i your-key.pem ./data_collect ubuntu@ec2-ip-address:/home/ubuntu/
```

---

### Step 2: Configure Environment Variables
Copy the template configuration file to a live `.env` file and edit it:
```bash
# Copy template
cp .env.example .env

# Edit env variables
nano .env
```
Inside the editor, update:
* `S3_BUCKET_NAME`: Set this to your S3 bucket (e.g., `my-quant-trading-data`).
* `S3_REGION`: Set this to your bucket's region (e.g., `us-east-1`).
* **AWS Access Keys**: Leave `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` blank if your EC2 instance is running with the IAM Role.
* *To save and exit Nano: Press `Ctrl+O` -> `Enter` -> `Ctrl+X`.*

---

### Step 3: Install Docker on the EC2 Host

#### 🔹 For Ubuntu Instances:
```bash
# 1. Update the packages list
sudo apt-get update -y

# 2. Install Docker
sudo apt-get install docker.io -y

# 3. Enable and start Docker service
sudo systemctl enable --now docker

# 4. Add your current user to the docker group
sudo usermod -aG docker $USER
```

#### 🔹 For Amazon Linux 2023 Instances:
```bash
# 1. Update the packages list
sudo dnf update -y

# 2. Install Docker
sudo dnf install docker -y

# 3. Enable and start Docker service
sudo systemctl enable --now docker

# 4. Add your current user to the docker group
sudo usermod -aG docker $USER
```

> [!IMPORTANT]
> **Apply Group Changes**: For the group settings to take effect, you **must close your SSH session and log back in**, or run the following command to refresh your shell group memberships:
> ```bash
> newgrp docker
> ```

---

### Step 4: Build and Start the Collector
Run Docker Compose in detached (background daemon) mode. It will automatically download Python 3.13-slim, build the layers, and launch the service:
```bash
docker compose up -d --build
```

---

## 🔍 Step 5: Operations, Monitoring & Verification

Because we mount a persistent host volume, you do not need to go inside the docker container to monitor or interact with your files.

### 1. View Live System Logs
Monitor the connection status of OKX/Binance, check WebSocket subscription streams, and verify loop health:
```bash
docker compose logs -f --tail 100
```
*(Press `Ctrl+C` to close the log stream; the container continues running in the background).*

### 2. Verify Folder Structures
Confirm that our `MarketDataWriter` is dynamically creating the daily storage hierarchies:
```bash
find local_cache/
```
You should see paths structured as:
`local_cache/{YYYYMMDD}/{exchange}/{symbol}/{market_type}/{category}.jsonl`

### 3. Tail Real-Time Trade Streams
Ensure trades are being buffered to disk successfully:
```bash
tail -f local_cache/$(date -u +%Y%m%d)/binance/BTCUSDT/spot/trades.jsonl
```
*(Press `Ctrl+C` to exit).*

---

## 🛠️ Step 6: Administration Commands

| Task | Command | Description |
| :--- | :--- | :--- |
| **Check Health** | `docker compose ps` | Displays the uptime and status of active container processes. |
| **Stop Daemon** | `docker compose down` | Stops the execution loop and closes all file handles gracefully. |
| **Restart App** | `docker compose restart` | Triggers a safe reload of the collector. |
| **View Host Storage**| `df -h` | Monitors EBS disk space utilization on your EC2 instance. |

---

## ❓ Troubleshooting Guide

### Issue 1: S3 Upload Fails with Permission Denied
* **Symptoms**: Logs show `NoCredentialsError` or `AccessDenied` when `uploader.py` attempts S3 uploads.
* **Fix**: Ensure that the IAM Role is associated with the EC2 instance. Navigate to **AWS Console -> EC2 -> Actions -> Security -> Modify IAM Role** and select your custom IAM role containing the correct S3 policy.

### Issue 2: `docker compose` command not found
* **Symptoms**: Running docker compose commands returns an execution error.
* **Fix**: Ensure your Docker version includes the V2 Compose plugin. If not, install it using:
  ```bash
  sudo mkdir -p /usr/local/lib/docker/cli-plugins
  sudo curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/lib/docker/cli-plugins/docker-compose
  sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
  ```
