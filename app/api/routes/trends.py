# app/api/routes/trends.py

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models.trend import Trend
from app.schemas.trend import TrendResponse
from app.services.trend_collector.youtube_trends import fetch_youtube_trends

router = APIRouter()


# 1) Main listing endpoint: /api/trends
@router.get("/trends", response_model=List[TrendResponse])
def get_trends(
    db: Session = Depends(get_db),
    metric: str = Query("youtube_trends", description="metric label, default youtube_trends"),
    date_: Optional[date] = Query(None, alias="date", description="Filter by date YYYY-MM-DD"),
):
    """
    Return latest trends for a metric.
    Default metric is 'youtube_trends'.
    """
    q = db.query(Trend).filter(Trend.metric == metric)
    if date_:
        q = q.filter(Trend.date == date_)
    q = q.order_by(Trend.value.desc()).limit(50)
    return q.all()


# 2) Debug endpoint: /api/trends/debug
@router.get("/trends/debug")
def debug_trends(db: Session = Depends(get_db)):
    """
    Raw view of the last 20 rows from trends table.
    Useful to confirm that cron / GitHub Action has inserted data.
    """
    rows = db.query(Trend).order_by(Trend.id.desc()).limit(20).all()
    return [
        {
            "id": r.id,
            "metric": r.metric,
            "date": str(r.date),
            "key": r.key,
            "value": r.value,
            "meta": r.meta,
        }
        for r in rows
    ]


# 3) Collector endpoint: /api/trends/youtube
@router.post("/trends/youtube")
def collect_youtube_trends(db: Session = Depends(get_db)):
    """
    Call YouTube API, normalize results, and store into 'trends' table.
    """
    trends = fetch_youtube_trends()

    if not trends:
        return {"inserted": 0}

    today = date.today()
    inserted = 0

    for t in trends:
        record = Trend(
            date=today,
            metric=t["metric"],
            key=t["key"],
            value=t["value"],
            meta=t.get("meta"),
        )
        db.add(record)
        inserted += 1

    db.commit()
    return {"inserted": inserted}
