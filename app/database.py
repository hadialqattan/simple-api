from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


# database URL and engine
SQLALCHEMY_DATABASE_URL = (
    "postgresql://"
    + os.environ["DB_OWNER"]
    + ":"
    + os.environ["DB_PASSWORD"]
    + "@"
    + os.environ["HnP"]
    + "/"
    + os.environ["DB"]
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# database session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base orm class
Base = declarative_base()
