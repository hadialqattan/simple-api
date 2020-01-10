from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


# database URL and engine
SQLALCHEMY_DATABASE_URL = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_POST']}/{os.environ['POSTGRES_DB']}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# database session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base orm class
Base = declarative_base()
