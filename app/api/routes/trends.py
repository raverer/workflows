from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from app.db.session import get_db
from app.db.models.trend import Trend

router = APIRouter()


# =============================
# GET /trends  → Fetch trends
# =============================
@router.get("/trends")
def get_trends(
    db: Session = Depends(get_db),
    date_: date = Query(None, alias="date"),
    metric: str = Query("google_top")
):
    q = db.query(Trend)

    if metric:
        q = q.filter(Trend.metric == metric)

    if date_:
        q = q.filter(Trend.date == date_)

    q = q.order_by(Trend.value.desc()).limit(50)

    results = q.all()

    return [
        {
            "id": r.id,
            "metric": r.metric,
            "date": str(r.date),
            "key": r.key,
            "value": r.value,
            "meta": r.meta,
        }
        for r in results
    ]


# ======================================
# GET /trends/debug → Quick DB inspection
# ======================================
@router.get("/trends/debug")
def debug_trends(db: Session = Depends(get_db)):
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
