from pytrends.request import TrendReq

def fetch_google_trends():
    pytrends = TrendReq(hl='en-US', tz=330)

    # Fetch "Trending Searches" for India
    trending_df = pytrends.trending_searches(pn='india')

    results = []
    for keyword in trending_df[0].tolist():
        results.append({
            "metric": "google_trends",
            "key": keyword,
            "value": 100,          # Google does not give a score, you can keep 100
            "meta": {"source": "google"}
        })

    return results
