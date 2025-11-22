# app/schemas/trend.py

from datetime import date
from typing import Any, Dict, Optional
from pydantic import BaseModel


class TrendBase(BaseModel):
    metric: str
    date: date
    key: str
    value: int
    meta: Optional[Dict[str, Any]] = None


class TrendResponse(TrendBase):
    id: int

    class Config:
        from_attributes = True  # for SQLAlchemy ORM models
