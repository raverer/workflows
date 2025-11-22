import requests
from bs4 import BeautifulSoup

def fetch_youtube_trends():
    url = "https://www.youtube.com/feed/trending"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception("Failed to fetch YouTube trends")

    soup = BeautifulSoup(response.text, "lxml")

    # Extract trending video titles
    titles = [tag.text.strip() for tag in soup.select("#video-title")]

    # Keep top 10 only
    top_items = titles[:10]

    trends = []
    for t in top_items:
        trends.append({
            "metric": "youtube_trends",
            "key": t,
            "value": 1,              # no numeric score available
            "meta": {"source": "youtube"}
        })

    return trends
