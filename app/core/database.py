from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:Frilancer2005@localhost:3306/kindly"

# Create the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured session class
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Create the declarative base
Base = declarative_base()

# Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

