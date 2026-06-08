# 🌐 Local Mock API Health Monitor

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Flask-Web_API-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img src="https://img.shields.io/badge/REST-API-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Monitoring-Health_Check-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Linux-Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" />
  <img src="https://img.shields.io/badge/Cybersecurity-Service_Monitoring-red?style=for-the-badge" />
</p>

---

# 📖 Overview

Modern applications rely heavily on APIs for communication between services. Monitoring API health is essential for maintaining reliability, availability, and performance.

In this lab, you will:

* 🚀 Create a local mock API service using Flask
* 🔍 Build an automated API health monitor
* ⏱️ Measure response times
* 📊 Track service availability
* 📝 Log health status information
* 🚨 Detect and report failures automatically

This project introduces concepts used in enterprise monitoring platforms such as Prometheus, Datadog, Nagios, and Splunk.

---

# 🎯 Learning Objectives

By completing this lab, you will be able to:

✅ Create a mock API service

✅ Implement REST API endpoints

✅ Monitor API availability

✅ Measure response times

✅ Log endpoint health information

✅ Detect service outages

✅ Analyze monitoring logs

✅ Generate endpoint status reports

---

# 📋 Prerequisites

Before starting, ensure you have:

* Linux Command Line Knowledge
* Basic Understanding of APIs
* Familiarity with Nano or Vim
* Understanding of HTTP Status Codes

### Common HTTP Status Codes

| Code | Meaning               |
| ---- | --------------------- |
| 200  | Success               |
| 201  | Created               |
| 400  | Bad Request           |
| 401  | Unauthorized          |
| 404  | Not Found             |
| 500  | Internal Server Error |

---

# 🛠️ Environment Setup

---

## 🚀 Install Required Tools

Update packages:

```bash
sudo apt update
```

Install Python:

```bash
sudo apt install -y python3 python3-pip
```

Install Flask and Requests:

```bash
pip3 install flask requests
```

Verify Installation:

```bash
python3 --version
pip3 --version
```

Expected Output:

```bash
Python 3.x.x
pip x.x.x
```

---

# 📁 Task 1 — Create Mock API Service

---

## 📂 Step 1: Create Project Structure

```bash
mkdir -p ~/api-health-monitor
cd ~/api-health-monitor

mkdir logs
mkdir mock-api
```

Verify:

```bash
tree .
```

Expected:

```text
.
├── logs
└── mock-api
```

---

## ⚙️ Step 2: Create Mock API Server

Create API file:

```bash
nano mock-api/api_server.py
```

Paste the API server code provided in the lab instructions.

---

## 🌐 API Endpoints

The API provides three endpoints:

### ❤️ Health Endpoint

```http
GET /health
```

Response:

```json
{
  "status": "healthy",
  "service": "mock-api"
}
```

---

### 👥 Users Endpoint

```http
GET /api/users
```

Features:

* Returns sample users
* Simulates failures every 5th request
* Simulates slow responses every 3rd request

---

### 📦 Data Endpoint

```http
GET /api/data
```

Features:

* Random response delay
* Simulates real-world API latency

---

## ▶️ Step 3: Start Mock API

Run:

```bash
python3 mock-api/api_server.py &
```

Save PID:

```bash
echo $! > api_pid.txt
```

Wait:

```bash
sleep 2
```

---

## 🧪 Step 4: Test API Endpoints

Health Check:

```bash
curl http://localhost:5000/health
```

Users Endpoint:

```bash
curl http://localhost:5000/api/users
```

Data Endpoint:

```bash
curl http://localhost:5000/api/data
```

Expected Output:

```json
{
  "status": "healthy"
}
```

---

# 🔍 Task 2 — Build the Health Monitor

---

## 📝 Step 1: Create Monitor Script

```bash
nano health_monitor.py
```

Paste the complete monitoring code provided in the lab instructions.

---

## 🔓 Step 2: Make Script Executable

```bash
chmod +x health_monitor.py
```

Verify:

```bash
ls -l health_monitor.py
```

Expected:

```text
-rwxr-xr-x
```

---

## ▶️ Step 3: Run the Health Monitor

```bash
python3 health_monitor.py
```

---

## 📊 Expected Console Output

```text
[2024-01-15 10:30:00] [INFO] Starting health monitor
[2024-01-15 10:30:00] [INFO] Monitoring endpoints
[2024-01-15 10:30:00] [INFO] --- Health Check #1 ---
[2024-01-15 10:30:00] [INFO] /health is healthy
[2024-01-15 10:30:01] [INFO] /api/users is healthy
```

---

# 🔬 Understanding the Health Monitor

---

## ⏱️ Response Time Monitoring

The monitor measures:

```python
start_time = time.time()
response = requests.get(url)
end_time = time.time()
```

Response time:

```python
(end_time - start_time) * 1000
```

Example:

```text
Response Time: 15.23ms
```

---

## 🟢 Healthy Endpoint

Status Codes:

```text
200 - 299
```

Example:

```text
200 OK
```

Logged As:

```text
healthy
```

---

## 🔴 Unhealthy Endpoint

Status Codes:

```text
400+
500+
```

Example:

```text
500 Internal Server Error
```

Logged As:

```text
unhealthy
```

---

## ⌛ Timeout Detection

The monitor detects:

```python
requests.exceptions.Timeout
```

Example:

```text
Request timed out
```

---

## 🌐 Connection Error Detection

Detects:

```python
requests.exceptions.ConnectionError
```

Example:

```text
Could not connect to service
```

---

# 📜 Viewing Logs

---

## View Log File

```bash
cat logs/health_monitor.log
```

---

## View Current Status

```bash
cat logs/current_status.json
```

---

## Real-Time Monitoring

```bash
tail -f logs/health_monitor.log
```

---

# 📈 Analyze Results

---

## Count Healthy Checks

```bash
grep "is healthy" logs/health_monitor.log | wc -l
```

---

## Count Failed Checks

```bash
grep "is unhealthy\|is error\|is timeout" logs/health_monitor.log | wc -l
```

---

## View Errors Only

```bash
grep "\[ERROR\]" logs/health_monitor.log
```

---

## Install jq for JSON Analysis

```bash
sudo apt install -y jq
```

---

## View Response Times

```bash
cat logs/current_status.json | jq '.endpoints[] | {endpoint: .endpoint, response_time: .response_time}'
```

Example:

```json
{
  "endpoint": "/health",
  "response_time": 14.25
}
```

---

# ✅ Verification

---

## Verify API Process

```bash
ps aux | grep api_server.py
```

Expected:

```text
python3 mock-api/api_server.py
```

---

## Verify Health Endpoint

```bash
curl -s http://localhost:5000/health | python3 -m json.tool
```

Expected:

```json
{
  "status": "healthy"
}
```

---

## Verify Log File

```bash
ls -lh logs/health_monitor.log
```

---

## Verify Log Entries

```bash
head -20 logs/health_monitor.log
```

Expected:

```text
[INFO] Health Check #1
[INFO] /health is healthy
```

---

## Verify Status File

```bash
cat logs/current_status.json | python3 -m json.tool
```

Expected:

```json
{
  "summary": {
    "total": 3,
    "healthy": 3,
    "unhealthy": 0
  }
}
```

---

## Verify Failure Detection

The mock API intentionally fails periodically.

Search logs:

```bash
grep -i "error\|unhealthy\|500" logs/health_monitor.log
```

Expected:

```text
/api/users is unhealthy
Status Code: 500
```

---

# 🧹 Cleanup

---

## Stop Mock API

```bash
kill $(cat api_pid.txt)
```

Verify:

```bash
ps aux | grep api_server.py
```

No running process should remain.

---

# 🛠️ Troubleshooting

---

## ❌ Connection Refused

Cause:

API server not running.

Solution:

```bash
python3 mock-api/api_server.py &
```

---

## ❌ Module Not Found

Install Dependencies:

```bash
pip3 install flask requests
```

---

## ❌ Port 5000 Already In Use

Find Process:

```bash
sudo lsof -ti:5000
```

Kill Process:

```bash
sudo lsof -ti:5000 | xargs kill -9
```

---

## ❌ Permission Denied

Fix Permissions:

```bash
chmod 755 logs/
```

---

# 📊 Monitoring Metrics Collected

The health monitor tracks:

| Metric        | Description            |
| ------------- | ---------------------- |
| Availability  | Is endpoint reachable? |
| Status Code   | HTTP response status   |
| Response Time | Endpoint latency       |
| Error Message | Failure reason         |
| Timestamp     | Time of check          |

---

# 🌍 Real-World Significance

Health monitoring is critical for:

* ☁️ Cloud Applications
* 🏢 Enterprise APIs
* 🔐 Security Operations
* 🚀 DevOps Pipelines
* 📡 Network Services
* 🛡️ Cybersecurity Monitoring

Production monitoring solutions use similar techniques to:

* Detect outages
* Alert administrators
* Measure SLA compliance
* Identify performance bottlenecks
* Ensure business continuity

---

# 🚀 Key Takeaways

✔️ APIs should be monitored continuously

✔️ Response times provide performance insights

✔️ Automated monitoring detects failures quickly

✔️ Logging enables troubleshooting and auditing

✔️ Health checks are essential for production systems

✔️ Service reliability depends on proactive monitoring

---

# 🏆 Lab Complete

Congratulations! 🎉

You successfully:

✅ Built a Mock REST API using Flask

✅ Implemented Multiple Endpoints

✅ Created an Automated Health Monitoring Tool

✅ Logged Availability and Response Times

✅ Detected Failures Automatically

✅ Generated Real-Time Status Reports

These skills form the foundation of modern observability, monitoring, and cybersecurity operations used in enterprise environments worldwide.

**Happy Monitoring! 🌐📊🚀**
