from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.db.models.trend import Trend
from datetime import date

router = APIRouter()

@router.get("/trends", response_model=List[dict])
def get_trends(db: Session = Depends(get_db),
               date_: date = Query(None, alias="date"),
               metric: str = Query("top_tags")):
    q = db.query(Trend).filter(Trend.metric == metric)
    if date_:
        q = q.filter(Trend.date == date_)
    q = q.order_by(Trend.value.desc()).limit(50)
    results = q.all()
    # convert to simple dicts or create pydantic models
    return [{"key": r.key, "value": r.value, "date": r.date.isoformat(), "meta": r.meta} for r in results]
