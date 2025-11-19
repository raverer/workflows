# app/db/base_models.py

from app.db.base import Base
from app.db.models.user import User
from app.db.models.trend import Trend

# Importing them ensures they get registered with Base.metadata