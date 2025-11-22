from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.db.session import get_db
from app.db.models.trend import Trend
from app.services.trend_collector.youtube_trends import fetch_youtube_trends

router = APIRouter()

# -------------------------------
# Collect YouTube Trends
# -------------------------------
@router.post("/youtube")
def collect_youtube_trends(db: Session = Depends(get_db)):
    trends = fetch_youtube_trends()

    for t in trends:
        record = Trend(
            date=date.today(),
            metric=t["metric"],
            key=t["key"],
            value=t["value"],
            meta=t["meta"]
        )
        db.add(record)

    db.commit()
    return {"inserted": len(trends)}


# -------------------------------
# Read Trends (for frontend users)
# -------------------------------
@router.get("/")
def get_trends(metric: str = "youtube_trends", db: Session = Depends(get_db)):
    rows = db.query(Trend).filter(Trend.metric == metric).all()

    return [
        {
            "id": r.id,
            "metric": r.metric,
            "date": r.date,
            "key": r.key,
            "value": r.value,
            "meta": r.meta
        }
        for r in rows
    ]


# -------------------------------
# Debug Route
# -------------------------------
@router.get("/debug")
def debug(db: Session = Depends(get_db)):
    rows = db.query(Trend).limit(20).all()
    return [
        {
            "id": r.id,
            "metric": r.metric,
            "date": str(r.date),
            "key": r.key,
            "value": r.value,
            "meta": r.meta
        }
        for r in rows
    ]
