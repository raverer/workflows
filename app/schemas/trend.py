from pydantic import BaseModel
from datetime import date
from typing import Any, Dict

class TrendResponse(BaseModel):
    id: int
    metric: str
    date: date
    key: str     # here video_id
    value: int   # view_count
    meta: Dict[str, Any]

    class Config:
        orm_mode = True
