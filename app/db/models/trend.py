from sqlalchemy import Column, Integer, String, Date, JSON
from app.db.base_class import Base

class Trend(Base):
    __tablename__ = "trends"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    metric = Column(String, index=True)
    key = Column(String)
    value = Column(Integer)
    meta = Column(JSON)
