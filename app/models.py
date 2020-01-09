from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB

# local import
from app.database import Base


class Config(Base):
    """
    configs table with two columns

    name: str (unique)
    
    metadata: nested key:value implemented as json
    """

    __tablename__ = "configs"

    name = Column(name="name", type_=String, primary_key=True)
    metadatac = Column(name="metadata", type_=JSONB)
