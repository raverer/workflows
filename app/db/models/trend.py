from sqlalchemy import Column, Integer, String, Date, Float, JSON
from app.db.base import Base

class Trend(Base):
    __tablename__ = "trends"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    metric = Column(String, index=True)
    key = Column(String, index=True)
    value = Column(Float)
    meta = Column(JSON, nullable=True)
