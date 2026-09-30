from app.models import Expense
from database import Base, engine

Base.metadata.create_all(bind=engine)
print("Database initialized and tables created.") 