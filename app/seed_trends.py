from datetime import date
from app.db.session import SessionLocal
from app.db.models.trend import Trend

db = SessionLocal()

sample_data = [
    {"date": date.today(), "metric": "top_tags", "key": "ai", "value": 92, "meta": "Artificial Intelligence"},
    {"date": date.today(), "metric": "top_tags", "key": "fastapi", "value": 75, "meta": "FastAPI Framework"},
    {"date": date.today(), "metric": "top_tags", "key": "marketing", "value": 60, "meta": "Marketing Trends"},
]

for item in sample_data:
    trend = Trend(
        date=item["date"],
        metric=item["metric"],
        key=item["key"],
        value=item["value"],
        meta=item["meta"]
    )
    db.add(trend)

db.commit()
db.close()

print("Seed data inserted successfully!")