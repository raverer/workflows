from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from app.db.session import get_db
from app.db.models.trend import Trend
from app.schemas.trend import TrendResponse
from app.services.trend_collector.google_trends import fetch_google_trends

router = APIRouter(prefix="/trends")

# ------------------------------------------------------
# POST /api/trends/google → Insert fresh trends
# ------------------------------------------------------
@router.post("/google")
def collect_google_trends(db: Session = Depends(get_db)):
    trends = fetch_google_trends()

    inserted = 0
    today = date.today()

    for t in trends:
        db.add(Trend(
            date=today,
            metric=t["metric"],
            key=t["key"],
            value=t["value"],
            meta=t["meta"]
        ))
        inserted += 1

    db.commit()
    return {"inserted": inserted}


# ------------------------------------------------------
# GET /api/trends → Query by date + metric
# ------------------------------------------------------
@router.get("/", response_model=List[TrendResponse])
def get_trends(
    db: Session = Depends(get_db),
    date_: date = Query(None, alias="date"),
    metric: str = Query("top_tags")
):
    q = db.query(Trend).filter(Trend.metric == metric)

    if date_:
        q = q.filter(Trend.date == date_)

    return q.order_by(Trend.value.desc()).limit(50).all()


# ------------------------------------------------------
# GET /api/trends/debug → see raw DB
# ------------------------------------------------------
@router.get("/debug")
def debug(db: Session = Depends(get_db)):
    rows = db.query(Trend).limit(20).all()

    return [
        {
            "id": r.id,
            "date": str(r.date),
            "metric": r.metric,
            "key": r.key,
            "value": r.value,
            "meta": r.meta,
        }
        for r in rows
    ]
