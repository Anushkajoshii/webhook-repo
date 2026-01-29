# GitHub Webhook Activity Monitor

This project is a Flask-based GitHub webhook receiver that listens to repository events, stores them in MongoDB, and displays recent activity in a simple auto-refreshing UI.

It is built as part of the Python Full Stack Developer assignment for Techstax Pvt. Ltd.

---

## 📌 Architecture Overview

```bash
GitHub Repository (action-repo)
|
| Webhook (push / PR / merge)
v
Cloudflare Tunnel (public URL)
|
v
Flask Webhook App (webhook-repo)
|
v
MongoDB (event storage)
|
v
HTML + JS UI (auto-refresh every 15s)
```


## 📁 Repositories

### 1. action-repo
Dummy GitHub repository used to trigger events:
- Push
- Pull Request
- Merge (optional)

### 2. webhook-repo (this repository)
Contains the Flask application that:
- Receives GitHub webhook events
- Stores minimal event data in MongoDB
- Displays recent events in a UI

---

## 🚀 Features

- GitHub webhook receiver (`/webhook`)
- Handles:
  - Push events
  - Pull request opened events
  - Merge events (bonus)
- Stores data in MongoDB
- Displays events in UI
- UI refreshes every 15 seconds
- Shows only new events (no duplicates)
- Time-window based filtering
- Uses UTC internally, displays local time

---

## 🛠️ Tech Stack

- Python 3
- Flask
- MongoDB
- HTML, CSS, JavaScript
- Cloudflare Tunnel (for webhook exposure)

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Anushkajoshii/webhook-repo.git
cd webhook-repo/app
```
### 2️⃣ Install dependencies
```bash
Copy code
pip install -r requirements.txt
```
### 3️⃣ Start MongoDB
```bash
brew services start mongodb-community
```
### 4️⃣ Run Flask app
```bash
python3 app.py
```
Flask runs on:
```bash
http://127.0.0.1:5000
```
### 5️⃣ Expose using Cloudflare Tunnel
```bash
cloudflared tunnel --url http://localhost:5000
```
Copy the generated public URL and use it in GitHub webhook settings.

🔗 GitHub Webhook Configuration (action-repo)
Payload URL:
```bash
https://<cloudflare-url>/webhook
```
Content type: application/json
Events: Send me everything
SSL verification: Enabled
Active: Yes

### 🖥️ UI
Open in browser:
```bash
http://127.0.0.1:5000/
```
The UI displays:

Author
Action (PUSH / PULL_REQUEST / MERGE)
To branch
Timestamp

Updates automatically every 15 seconds.

### 📹 Demo Video
A short demo video is recorded showing:

Webhook setup

Push event from action-repo

Event appearing in MongoDB

UI updating automatically

(Shared via Google Drive link in submission form.)

### ✅ Assignment Status
 Two repositories created

 GitHub webhook receiver implemented

 MongoDB integration

 UI with polling and time filtering

 No duplicate events

 Optional merge event handled

### 👤 Author
Anushka Joshi
GitHub: https://github.com/Anushkajoshii
