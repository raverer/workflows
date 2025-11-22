from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List
from app.db.session import get_db
from app.db.models.trend import Trend
from app.schemas.trend import TrendSchema

router = APIRouter()

# ---------------------
# GET /api/trends
# ---------------------
@router.get("/trends")
def get_trends(
    db: Session = Depends(get_db),
    date_: date = Query(None, alias="date"),
    metric: str = Query("google_trends")
):
    q = db.query(Trend).filter(Trend.metric == metric)

    if date_:
        q = q.filter(Trend.date == date_)

    q = q.order_by(Trend.value.desc())
    rows = q.all()

    if not rows:
        return {"message": "No trends found"}

    return {
        "date": str(rows[0].date),
        "source": rows[0].metric.replace("_trends", ""),
        "trends": [
            {"topic": r.key, "score": r.value}
            for r in rows
        ]
    }


# ---------------------
# DEBUG: GET /api/trends/debug
# ---------------------
@router.get("/trends/debug")
def debug(db: Session = Depends(get_db)):
    rows = db.query(Trend).order_by(Trend.id.desc()).limit(20).all()
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


# ---------------------
# POST /api/trends/google
# ---------------------
@router.post("/trends/google")
def collect_google_trends(db: Session = Depends(get_db)):
    from app.services.trend_collector.google_trends import fetch_google_trends

    trends = fetch_google_trends()
    today = date.today()

    for t in trends:
        record = Trend(
            date=today,
            metric=t["metric"],
            key=t["key"],
            value=t["value"],
            meta=t["meta"],
        )
        db.add(record)

    db.commit()
    return {"inserted": len(trends)}
