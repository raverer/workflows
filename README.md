📈 Trend Collection API
Daily Automated YouTube Trend Collector + REST API (FastAPI + PostgreSQL + GitHub Actions + Render)

A production-ready microservice for collecting & serving daily trending data.

🚀 Overview

This project is a fully deployed, automated trend-tracking backend that:

✔ Fetches daily trending YouTube videos (Top 20)
✔ Stores them in a PostgreSQL database
✔ Provides a live REST API for consumers
✔ Includes secure user authentication (JWT)
✔ Uses GitHub Actions to run daily cron jobs
✔ Is deployed on Render with zero downtime

This demonstrates end-to-end backend engineering skills, including:

API design (FastAPI)

Authentication (JWT, hashed passwords)

Database design (SQLAlchemy + Postgres)

Background automation (GitHub Actions CRON)

Cloud deployment (Render)

External API integrations (YouTube Data API)

🌐 Live Demo (Deployed on Render)
Endpoint	Description
https://workflows-1.onrender.com/	API Home
/docs	Swagger UI (interactive API docs)
/auth/signup	Create a user
/auth/login	Login & get JWT token
/api/trends/youtube — POST	Collect latest YouTube trends
/api/trends/trends — GET	Query trends as an end user
/api/trends/trends/debug — GET	Debug raw DB rows
⚙ Architecture
FastAPI backend
 ├── Authentication (JWT)
 ├── Trends module
 │    ├── YouTube API integration
 │    ├── Normalized trend storing
 │    └── API for fetching trends
 ├── SQLAlchemy ORM models
 ├── PostgreSQL database (Render)
 └── GitHub Actions CRON → hits POST /api/trends/youtube daily

🛠 Features
📌 1. Collects YouTube Trending Videos

Uses the YouTube Data API v3:

Video title

Channel name

Publish date

View count

Video ID

Region-based filtering

📌 2. Stores Trends in PostgreSQL

Each trend record contains:

{
  "metric": "youtube_trends",
  "key": "VIDEO_ID",
  "value": 12345678,
  "meta": {
    "source": "youtube",
    "title": "Video Title",
    "channel_title": "Channel Name",
    "published_at": "ISO_TIMESTAMP"
  }
}

📌 3. Public API for Consumers

Developers can:

Fetch today’s trends

Filter by date

Filter by metric

Build dashboards or analytics

📌 4. Fully Automated

Daily automation:

GitHub Actions cron job

Hits Render POST endpoint

Saves fresh trends every day

No manual work required.

🧩 Tech Stack
Category	Technology
Backend Framework	FastAPI
Language	Python
Database	PostgreSQL (Render)
ORM	SQLAlchemy
Auth	JWT
API Client	YouTube Data API
Automation	GitHub Actions
Deployment	Render Web Service
📦 Folder Structure
app/
 ├── api/routes
 │    └── trends.py
 │    └── auth.py
 ├── db/
 │    ├── models/
 │    │     └── trend.py
 │    │     └── user.py
 │    ├── base.py
 │    ├── session.py
 ├── schemas/
 │    └── trend.py
 ├── services/
 │    └── trend_collector/
 │           └── youtube_trends.py
 ├── main.py

🧪 API Usage Examples
🔹 Fetch today’s trends
GET /api/trends/trends

🔹 Fetch for a specific date
GET /api/trends/trends?date=2025-11-22

🔹 Collect new trends (admin/internal use)
POST /api/trends/youtube

🔹 Inspect DB directly
GET /api/trends/trends/debug

🤖 GitHub Actions (Automated CRON)

.github/workflows/daily-trends.yml

name: Daily Trend Collection

on:
  schedule:
    - cron: "0 3 * * *"
  workflow_dispatch:

jobs:
  collect_trends:
    runs-on: ubuntu-latest
    steps:
    - name: Trigger Trend Collection
      run: |
        curl -X POST "${{ secrets.TRENDS_URL }}" \
        -H "Content-Type: application/json"

🌱 Environment Variables (Render Dashboard)
Variable	Example
DATABASE_URL	postgres://…
YOUTUBE_API_KEY	AIzaSy…
YOUTUBE_REGION	IN
🧑‍💻 Local Development
git clone your-repo
cd your-repo

pip install -r requirements.txt

uvicorn app.main:app --reload

🎯 What This Project Demonstrates (For Recruiters)

This repository showcases:

✔ Backend Development

Designing APIs, routing, modular architecture.

✔ Cloud Deployment

Live service with correct environment configs.

✔ Automation Engineering

Cron-based scheduled data ingestion using GitHub Actions.

✔ Data Modeling

Database schema design and migrations.

✔ API Integration

Working with external APIs (YouTube).

✔ Production Best Practices

JWT auth

ENV variable handling

Isolated services

Clean folder structure

⭐ Why This Project Matters

This system can be extended into:

Trend dashboards

Data analytics platforms

Social media research tools

Creator-focused insights

Competitor analysis tools

Viral prediction engines

And yes — it can be monetized through:

API subscriptions

Dashboards

Daily emailed insights

"Trending topics intelligence" SaaS
