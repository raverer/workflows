# file: app/db/create_tables.py
from app.db.session import engine
from app.db.base import Base   # or base_class depending how you named it
# import all models so they're registered
import app.db.models.user
import app.db.models.trend

def create_all():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_all()
    print("tables created")