from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# local import
from . import crud, models, schemas
from app.database import SessionLocal, engine

# create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Endpoints

@app.get('/configs')
def list(db: Session = Depends(get_db)):
    """
    SQL query: SELECT * FROM configs;
    
    summary: list all configs
    
    get_args: None
    
    return: valid json contain all configs table rows
    """
    # select all configs
    configs = crud.get_configs(db=db)
    # convert str metadata to dict
    configs_list = [{"name":config.name, "metadata":eval(config.metadatac)} for config in configs]
    # check for empty configs table
    return {"Configs":configs_list} if configs_list else {"Configs":"Empty"}


@app.post('/configs')
def create(config:schemas.ConfigCreate, db: Session = Depends(get_db)):    
    """
    SQL query: INSERT INTO configs (name, metadata) VALUES (nameValue, metadataValue)
    
    summary: create new config into configs table

    arguments: (config: schemas.ConfigCeate [an instance of ConfigCreate class])

    return: json response contain success message or failed message with 400 
    """
    # get config by name
    db_config = crud.get_config(name=config.name, db=db)
    # check for exists config
    if db_config:
        raise HTTPException(status_code=400, detail="name already exists")
    # create new config 
    new_config = crud.create_config(config=config, db=db)
    return {"New config has created": {"name":config.name, "metadata":config.metadata}}


@app.get('/configs/{name}')
def get(name:str, db: Session = Depends(get_db)):
    """
    SQL query: SELECT * FROM configs WHERE name=name;

    summary: get config by name

    arguments: (name:str [config name])

    return: json response if name exists else failed message with 404
    """
    # get config by name
    config = crud.get_config(name=name, db=db)
    # check for unexists name
    if not config:
        raise HTTPException(status_code=404, detail="name doesn't exists")
    # convert str metadata to key:value
    return {"Config":{"name":config.name, "metadata":eval(config.metadatac)}}


@app.put('/configs/{name}')
def update(name:str, metadata:dict, db: Session = Depends(get_db)):
    """
    SQL query: UPDATE configs SET metadata=metadata WHERE name=name;

    summary: update config by name

    arguments: (name: str [config name]), (metadata: str [config metadata])

    return: json response
    """
    # create new config with update value
    config_schema = schemas.ConfigUpdate(name=name, metadata=metadata)
    # update the config with new metadata value
    db_config = crud.update_config(config=config_schema, db=db)
    # check for unexists name
    if not db_config:
        raise HTTPException(status_code=404, detail="name doesn't exists")
    # return success response
    return {"The config has updated": {"name":config_schema.name, "metadata":config_schema.metadata}}


@app.delete('/configs/{name}')
def delete(name:str, db: Session = Depends(get_db)):
    """
    SQL query: DELETE FROM configs WHERE name=name;

    summary: delete config by name

    arguments: (name: str [config name])

    return: json succeed message if config has deleted else failed message if config doesn't exists
    """
    # delete config by name
    success = crud.delete_config(name=name, db=db)
    # check for unexists name
    if not success:
        raise HTTPException(status_code=404, detail="name doesn't exists")
    return {"The config has deleted": {"name":name}}
