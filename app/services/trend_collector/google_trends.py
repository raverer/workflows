# app/services/trend_collector/google_trends.py

from pytrends.request import TrendReq

def fetch_google_trends():
    pytrend = TrendReq(hl="en-US", tz=330)

    pytrend.build_payload(kw_list=["ai", "technology", "news"], timeframe="now 1-d")
    data = pytrend.interest_over_time()

    if data.empty:
        return []

    trends = []
    for keyword in data.columns[:-1]:  # skip 'isPartial'
        value = int(data[keyword].iloc[-1])
        trends.append({
            "metric": "google_trends",
            "key": keyword,
            "value": value,
            "meta": {"source": "google"}
        })
    return trends
