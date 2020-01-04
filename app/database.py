from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# database URL and engine
SQLALCHEMY_DATABASE_URL = "postgresql://api_owner:api112233@localhost/apidb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# database session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base orm class
Base = declarative_base()
