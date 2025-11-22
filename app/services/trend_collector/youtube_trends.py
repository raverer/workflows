# app/services/trend_collector/youtube_trends.py

import os
from googleapiclient.discovery import build  # Requires: google-api-python-client

# Environment variables (set these in Render Dashboard → Environment)
API_KEY = os.getenv("YOUTUBE_API_KEY")
REGION_CODE = os.getenv("YOUTUBE_REGION", "IN")  # Default region: India


def fetch_youtube_trends(max_results: int = 20):
    """
    Fetch trending (most popular) YouTube videos for a region.

    - Uses YouTube Data API v3 (free tier).
    - Returns normalized dicts ready for insertion into the `Trend` table.
    - No thumbnails (as requested).
    """

    if not API_KEY:
        raise RuntimeError(
            "YOUTUBE_API_KEY is missing. Set it in your Render environment."
        )

    # Build the YouTube API client
    youtube = build("youtube", "v3", developerKey=API_KEY)

    # Fetch trending videos
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode=REGION_CODE,
        maxResults=max_results,
    )

    response = request.execute()
    items = response.get("items", [])

    trends = []

    for item in items:
        vid = item.get("id")
        snippet = item.get("snippet", {}) or {}
        stats = item.get("statistics", {}) or {}

        title = snippet.get("title")
        channel_title = snippet.get("channelTitle")
        publish_time = snippet.get("publishedAt")  # ISO timestamp
        view_count = int(stats.get("viewCount", 0))

        trends.append(
            {
                "metric": "youtube_trends",   # will go into Trend.metric
                "key": vid,                   # Trend.key
                "value": view_count,          # Trend.value
                "meta": {                     # Trend.meta
                    "source": "youtube",
                    "title": title,
                    "channel_title": channel_title,
                    "published_at": publish_time,
                },
            }
        )

    return trends
