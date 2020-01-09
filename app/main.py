from fastapi import FastAPI, Depends, HTTPException, Body
from starlette.requests import Request
from sqlalchemy.orm import Session

# local import
from app.crud import (
    get_configs,
    get_config,
    create_config,
    update_config,
    delete_config,
    query_metadata,
)
from app.database import SessionLocal, engine
from app.schemas import ConfigCreate, ConfigUpdate
from app.models import Base


# create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Endpoints


@app.get("/configs")
def List(db: Session = Depends(get_db)):
    """
    SQL query: SELECT * FROM configs;
    
    summary: list all configs
    
    arguments: None
    
    return: valid json contain all configs table rows
    """
    # select all configs
    configs = get_configs(db=db)
    # convert metadatac to metadata
    configslist = [
        {"name": config.name, "metadata": config.metadatac} for config in configs
    ]
    # check for empty configs table
    return {"Configs": configslist} if configs else {"Configs": "Empty"}


@app.post("/configs")
def Create(config: ConfigCreate, db: Session = Depends(get_db)):
    """
    SQL query: INSERT INTO configs (name, metadata) VALUES (nameValue, metadataValue)
    
    summary: create new config into configs table

    arguments: (config: ConfigCeate [an instance of ConfigCreate class])

    return: json response contain success message or failed message with 400 
    """
    # check for exists config
    if get_config(name=config.name, db=db):
        raise HTTPException(status_code=400, detail="name already exists")
    # create new config
    new_config = create_config(config=config, db=db)
    return {
        "New config has created": {"name": config.name, "metadata": config.metadata}
    }


@app.get("/configs/{name}")
def Get(name: str, db: Session = Depends(get_db)):
    """
    SQL query: SELECT * FROM configs WHERE name=name;

    summary: get config by name

    arguments: (name:str [config name])

    return: json response if name exists else failed message with 404
    """
    # get config by name
    config = get_config(name=name, db=db)
    # check for unexists name
    if not config:
        raise HTTPException(status_code=404, detail="name doesn't exists")
    # convert metadatac to metadata
    return {"Config": {"name": config.name, "metadata": config.metadatac}}


@app.put("/configs/{name}")
def Update(name: str, metadata: dict, db: Session = Depends(get_db)):
    """
    SQL query: UPDATE configs SET metadata=metadata WHERE name=name;

    summary: update config by name

    arguments: (name: str [config name]), (metadata: str [config metadata])

    return: json response
    """
    # create new config with update value
    config_schema = ConfigUpdate(name=name, metadata=metadata)
    # update the config with new metadata value
    db_config = update_config(config=config_schema, db=db)
    # check for unexists name
    if not db_config:
        raise HTTPException(status_code=404, detail="name doesn't exists")
    # return success response
    return {"The config has updated": config_schema}


@app.delete("/configs/{name}")
def Delete(name: str, db: Session = Depends(get_db)):
    """
    SQL query: DELETE FROM configs WHERE name=name;

    summary: delete config by name

    arguments: (name: str [config name])

    return: json succeed message if config has deleted else failed message if config doesn't exists
    """
    # delete config by name
    success = delete_config(name=name, db=db)
    # check for unexists name
    if not success:
        raise HTTPException(status_code=404, detail="name doesn't exists")
    return {"The config has deleted": {"name": name}}


@app.get("/search/metadata.{key}={value}")
def Query(key: str, value: str, db: Session = Depends(get_db)):
    """
    SQL query: SELECT * FROM configs WHERE (configs.metadata #>> %(metadata_1)s) = %(param_1)s;

    summary: get all configs has specific metadata by nested key and value

    arguments: (query param: str [metadata.keys...=value])

    return: valid json contain all configs matched by metadata search
    """
    # fetch query keys from query params
    keys = key.split(".")
    # get all matched configs
    configs = query_metadata(keys=key, value=value, db=db)
    # convert metadatac to metadata
    configslist = [
        {"name": config.name, "metadata": config.metadatac} for config in configs
    ]
    # check for empty configs
    return {"Configs": configslist} if configs else {"Configs": "Empty"}
