from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.db.session import get_db
from app.db.models.trend import Trend
from app.services.trend_collector.google_trends import fetch_google_trends

router = APIRouter()

@router.post("/google")
def collect_google_trends(db: Session = Depends(get_db)):
    trends = fetch_google_trends()

    for t in trends:
        row = Trend(
            date=date.today(),
            metric=t["metric"],
            key=t["key"],
            value=t["value"],
            meta=t["meta"]
        )
        db.add(row)

    db.commit()
    return {"inserted": len(trends)}
