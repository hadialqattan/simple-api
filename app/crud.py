"""
CRUD comes from: Create, Read, Update, and Delete.
"""

from sqlalchemy.orm import Session

# local import
import models, schemas


def get_configs(db: Session):
    """ 
    designed for [List : GET : /configs] endpoint

    SQL query: SELECT * FROM configs;

    summary: list all configs

    arguments: (db: Session [sqlalchemy database session])

    return: all configs table rows
    """
    return db.query(models.Config).all()


def create_config(db: Session, config: schemas.ConfigCreate):
    """
    designed for [Create : POST : /configs]

    SQL query: INSERT INTO configs (name, metadatac) VALUES (nameValue, metadatacValue)

    summary: create new config into configs table

    arguments: (db: Session [sqlalchemy database session]), (config: schemas.ConfigCeate [an instance of ConfigCreate class])

    return: new config
    """
    db_config = models.Config(name=config.name, metadatac=dict(config.metadata))
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config


def get_config(db: Session, name: str):
    """ 
    designed for [GET : GET : /configs/{name}] endpoint
    
    SQL query: SELECT * FROM configs WHERE name=name;

    summary: get config by name

    arguments: (db: Session [sqlalchemy database session]), (name: str [config name])

    return: single config
    """
    return db.query(models.Config).filter(models.Config.name == name).first()


def update_config(db: Session, config: schemas.ConfigUpdate):
    """ 
    designed for [Update : PUT : /configs/{name}]

    SQL query: UPDATE configs SET metadata=metadata WHERE name=name;

    summary: update config by name

    arguments: (db: Session [sqlalchemy database session]), (config: schemas.ConfigUpdate [an instance of ConfigUpdate class])

    return: updated config or false if config doesn't exists
    """
    db_config = (
        db.query(models.Config).filter(models.Config.name == config.name).first()
    )
    if not db_config:
        return False
    db_config.metadatac = config.metadata
    db.commit()
    db.refresh(db_config)
    return db_config


def delete_config(db: Session, name: str):
    """
    designed for [Delete : DELETE : /configs/{name}] 

    SQL query: DELETE FROM configs WHERE name=name;

    summary: delete config by name

    arguments: (db: Session [sqlalchemy database session]), (name: str [config name])

    return: True if config exits else False
    """
    db_config = db.query(models.Config).filter(models.Config.name == name).first()
    if not db_config:
        return False
    db.delete(db_config)
    db.commit()
    return True
