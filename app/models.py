from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

# local import
from .database import Base


class Config(Base):
    """
    configs table with five columns

    id: int 
    
    owner: int (owner username)

    name: str (unique for user)
    
    metadata: nested key:value implemented as json

    note: str
    """

    __tablename__ = "configs"

    id = Column(name="id", type_=Integer, primary_key=True)
    owner = Column(ForeignKey("users.username"), name="owner", type_=String(50))
    name = Column(name="name", type_=String(120))
    metadatac = Column(name="metadata", type_=JSONB)
    note = Column(name="note", type_=String)


class User(Base):
    """
    users table with one-to-many relationship with cofigs table 

    username: str (user name)

    password: str (user password)

    isadmin: bool
    """

    __tablename__ = "users"

    username = Column(name="username", type_=String(50), primary_key=True)
    password = Column(name="password", type_=String(80))
    isadmin = Column(name="isadmin", type_=Boolean)
    configs = relationship("Config")
