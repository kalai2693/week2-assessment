
from sqlalchemy import create_engine
from models import Base

DATABASE_URL = "postgresql+psycopg2://postgres:NewStrongPassword123!@localhost:5432/postgres"

engine = create_engine(DATABASE_URL, echo=True)

def create_tables():
    Base.metadata.create_all(engine)
    print("SQLAlchemy tables created successfully!")

if __name__ == "__main__":
    create_tables()
