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
@router.post("/trends/youtube")
def collect_youtube_trends(db: Session = Depends(get_db)):
    """
    Call YouTube API → normalize → save into DB.
    """

    trends = fetch_youtube_trends()

    if not trends:
        return {"inserted": 0}

    today = date.today()
    inserted = 0

    for t in trends:
        # FIXED mapping according to your youtube_trends.py structure
        record = Trend(
            date=today,
            metric="youtube_trends",
            key=t["video_id"],          # correct field name
            value=t["view_count"],      # correct field name
            meta=t.get("meta", {}),
        )
        db.add(record)
        inserted += 1

    db.commit()
    return {"inserted": inserted}
