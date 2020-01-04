from sqlalchemy import Column, String, JSON

# local import
from database import Base


class Config(Base):
    """
    configs table with two columns

    name: str (unique)
    
    metadata: nested key:value implemented as json
    """

    __tablename__ = "configs"

    name = Column('name', String, primary_key=True)
    metadatac = Column('metadata', JSON)
