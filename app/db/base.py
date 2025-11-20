# app/db/base.py

from .base_class import Base  # <-- FIXED IMPORT
from app.db.models.trend import Trend
from app.db.models.user import User

# This file ensures all models are imported so Base.metadata.create_all works
