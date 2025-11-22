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


# --------------------------------------------
# 1) GET /api/trends  → view trends
# --------------------------------------------
@router.get("/trends", response_model=List[TrendResponse])
def get_trends(
    db: Session = Depends(get_db),
    metric: str = Query("youtube_trends", description="metric label, default youtube_trends"),
    date_: Optional[date] = Query(None, alias="date", description="Filter by date YYYY-MM-DD"),
):
    """
    Return the latest stored trends (defaults to YouTube trending videos).
    """

    q = db.query(Trend).filter(Trend.metric == metric)

    if date_:
        q = q.filter(Trend.date == date_)

    q = q.order_by(Trend.value.desc()).limit(50)
    return q.all()


# --------------------------------------------
# 2) GET /api/trends/debug → inspect raw DB data
# --------------------------------------------
@router.get("/trends/debug")
def debug_trends(db: Session = Depends(get_db)):
    """
    Show last 20 rows from DB — useful to verify GitHub cron inserts are working.
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


# --------------------------------------------
# 3) POST /api/trends/youtube  → collect & insert live trends
# --------------------------------------------
@router.post("/youtube")
def collect_youtube_trends(db: Session = Depends(get_db)):
    trends = fetch_youtube_trends()

    if not trends:
        return {"inserted": 0}

    for t in trends:
        record = Trend(
            date=date.today(),
            metric=t["metric"],   # "youtube_trends"
            key=t["key"],         # VIDEO ID
            value=t["value"],     # VIEW COUNT
            meta=t["meta"]        # title, channel, publish date
        )
        db.add(record)

    db.commit()
    return {"inserted": len(trends)}
