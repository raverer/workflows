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
    from app.services.trend_collector.youtube_trends import fetch_youtube_trends
    trends = fetch_youtube_trends(max_results=20)
    for t in trends:
        record = Trend(
            date=date.today(),
            metric=t["metric"],
            key=t["video_id"],
            value=t["view_count"],
            meta=t["meta"]
        )
        db.add(record)
    db.commit()
    return {"inserted": len(trends)}

@router.get("/youtube", response_model=List[TrendResponse]) 
def get_youtube_trends(db: Session = Depends(get_db)):
    rows = db.query(Trend).filter(Trend.metric == "youtube_trends").order_by(Trend.value.desc()).limit(50).all()
    return rows

