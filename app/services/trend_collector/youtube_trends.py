import os
from googleapiclient.discovery import build  # You’ll install `google-api-python-client`
from datetime import date

API_KEY = os.getenv("YOUTUBE_API_KEY")
REGION_CODE = os.getenv("YOUTUBE_REGION", "IN")

def fetch_youtube_trends(max_results: int = 10):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode=REGION_CODE,
        maxResults=max_results
    )
    response = request.execute()
    trends = []
    for item in response.get("items", []):
        trends.append({
            "video_id": item["id"],
            "title": item["snippet"]["title"],
            # thumbnail excluded on purpose:
            "view_count": int(item["statistics"].get("viewCount", 0)),
            "publish_date": item["snippet"]["publishedAt"],
            "metric": "youtube_trends",
            "meta": {"source": "youtube"}
        })
    return trends
