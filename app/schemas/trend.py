from pydantic import BaseModel
from datetime import date
from typing import Optional, Any

class TrendSchema(BaseModel):
    id: int
    date: date
    metric: str
    key: str
    value: int
    meta: Optional[Any]

    class Config:
        from_attributes = True
