# app/services/trend_collector/youtube_trends.py

import os
from googleapiclient.discovery import build  # make sure google-api-python-client is in requirements

API_KEY = os.getenv("YOUTUBE_API_KEY")
REGION_CODE = os.getenv("YOUTUBE_REGION", "IN")  # default India


def fetch_youtube_trends(max_results: int = 20):
    """
    Fetch top 'most popular' YouTube videos for a region.
    - No thumbnails returned (per your request).
    - We return a normalized list of dicts that the Trend model can store.
    """
    if not API_KEY:
        # This will surface as a 500 in the FastAPI route – that’s fine, it’s a clear error.
        raise RuntimeError("YOUTUBE_API_KEY environment variable is not set")

    youtube = build("youtube", "v3", developerKey=API_KEY)

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

        title = snippet.get("title", "")
        channel_title = snippet.get("channelTitle", "")
        publish_at = snippet.get("publishedAt")  # ISO string
        view_count = int(stats.get("viewCount", 0))

        trends.append(
            {
                "metric": "youtube_trends",
                "key": vid,          # goes into Trend.key
                "value": view_count, # goes into Trend.value
                "meta": {
                    "source": "youtube",
                    "title": title,
                    "channel_title": channel_title,
                    "published_at": publish_at,
                },
            }
        )

    return trends
