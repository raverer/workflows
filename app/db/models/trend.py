# app/db/models/trend.py

from sqlalchemy import Column, Integer, String, Date, JSON
from app.db.base_class import Base


class Trend(Base):
    __tablename__ = "trends"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)              # when we stored this trend snapshot
    metric = Column(String, index=True, nullable=False)  # e.g. "youtube_trends"
    key = Column(String, index=True, nullable=False)     # e.g. video_id
    value = Column(Integer, nullable=False)          # e.g. view_count
    meta = Column(JSON, nullable=True)               # extra data (title, channel, etc.)
