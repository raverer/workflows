from pydantic import BaseModel
from datetime import date
from typing import Optional, Dict, Any

class TrendResponse(BaseModel):
    id: int
    metric: str
    date: date
    key: str
    value: int
    meta: Dict[str, Any]

    class Config:
        from_attributes = True
