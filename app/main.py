from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import List

# local import
from . import crud, schemas, database, auth, models, settings


# create the database tables
database.Base.metadata.create_all(bind=database.engine)

# init the app
app = FastAPI()


# Dependency
def get_db():
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()


# create admin
settings.create_admin()


# Endpoints

# auth


@app.post(
    "/token",
    response_model=schemas.Token,
    responses={401: {"detail": "Incorrect username or password"}},
)
async def get_access_token(
    db: Session = Depends(get_db), form_data: auth.OAuth2PasswordRequestForm = Depends()
):
    """
    summary: generate access token

    arguments: (db: Session), (form_data: OAuth2PasswordRequestForm)

    return: access token 
    """
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=auth.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# users


@app.get("/users/me/", response_model=schemas.UserRead)
def GetMe(current_user: schemas.UserRead = Depends(auth.get_current_user)):
    """
    SQL query: SELECT * FROM users WHERE username=username;

    summary: read current user data

    arguments: (current_user: schemas.UserRead)

    return: current user
    """
    return current_user.__dict__


@app.get(
    "/users",
    responses={
        401: {"detail": "Only admins can perform this function"},
        200: {"Users": List[schemas.UserRead]},
    },
)
def ListUsers(
    current_user: schemas.UserRead = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    """
    SQL query: SELECT * FROM users WHERE;

    summary: get all users (admin function)

    arguments: (current_user: schemas.UserRead = Depends(auth.get_current_user)), (db: Session = Depends(get_db))

    return: users table
    """
    # check for admin
    if not current_user.isadmin:
        raise HTTPException(
            status_code=401, detail="Only admins can perform this function"
        )
    # select all users
    users = crud.get_users(db=db)
    return {
        "Users": [
            {
                "username": user.username,
                "isadmin": user.isadmin,
                "configs": user.configs,
            }
            for user in users
        ]
    }


@app.get(
    "/users/admins",
    responses={
        401: {"detail": "Only admins can perform this function"},
        200: {"Users": List[schemas.UserRead]},
    },
)
def GetAdmins(
    current_user: schemas.UserRead = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    """
    SQL query: DELETE FROM users WHERE isadmin=true;

    summary: get all admins

    arguments: (current_user: schemas.UserRead = Depends(auth.get_current_user)), (db: Session = Depends(get_db))

    return: json message contain admins
    """
    # check for admin
    if not current_user.isadmin:
        raise HTTPException(
            status_code=401, detail="Only admins can perform this function"
        )
    admins = crud.get_admins(db=db)
    return {
        "Admins": [
            {
                "username": user.username,
                "isadmin": user.isadmin,
                "configs": user.configs,
            }
            for user in admins
        ]
    }


@app.post(
    "/user",
    responses={
        400: {"detail": "username already exists"},
        401: {"detail": "Only admins can perform this function"},
        200: {"created": schemas.UserRead},
    },
)
def CreateUser(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserRead = Depends(auth.get_current_user),
):
    """
    SQL query: INSERT INTO users (username, password, isadmin) VALUES (usrenameValue, passwordHashValue, isadminValue)
    
    summary: create new config into configs table

    arguments: (user: UserCreate [an instance of UserCreate class])

    return: json response contain success message or failed message with 400
    """
    # check for admin
    if not current_user.isadmin:
        raise HTTPException(
            status_code=401, detail="Only admins can perform this function"
        )
    # check for exists username
    if crud.get_user(db=db, username=user.username):
        raise HTTPException(status_code=400, detail="username already exists")
    # create new user
    new_user = crud.create_user(db=db, user=user)
    return {
        "created": {
            "username": new_user.username,
            "isadmin": new_user.isadmin,
            "configs": new_user.configs,
        }
    }


@app.get(
    "/user/{username}",
    response_model=schemas.UserRead,
    responses={
        401: {"detail": "Only admins can perform this function"},
        404: {"detail": "The user doesn't exists"},
    },
)
def GetUser(
    username: str,
    current_user: schemas.UserRead = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    """
    SQL query: SELECT * FROM users WHERE username=username;

    summary: get user by username (admin function)

    arguments: (username: str), (current_user: schemas.UserRead = Depends(auth.get_current_user)), (db: Session = Depends(get_db))

    return: json message contain the user if exsist
    """
    # check for admin
    if not current_user.isadmin:
        raise HTTPException(
            status_code=401, detail="Only admins can perform this function"
        )
    user = crud.get_user(db=db, username=username)
    # check if the user exsist
    if not user:
        raise HTTPException(status_code=404, detail="The user doesn't exists")
    return user.__dict__


@app.put(
    "/user/{username}/{set_admin}",
    responses={
        401: {"detail": "Only admins can perform this function"},
        404: {"detail": "The user doesn't exists"},
        200: {"Updated": schemas.UserRead},
    },
)
def UpdateUser(
    username: str,
    set_admin: bool,
    current_user: schemas.UserRead = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    """
    SQL query: UPDATE users SET isadmin=isadmin WHERE username=username;

    summary: update user details (admin function)

    arguments: (username: str), (set_admin: bool), (current_user: schemas.UserRead = Depends(auth.get_current_user)), (db: Session = Depends(get_db))

    return: json success message with new user info
    """
    # check for admin
    if not current_user.isadmin:
        raise HTTPException(
            status_code=401, detail="Only admins can perform this function"
        )
    user = crud.update_user(db=db, username=username, isadmin=set_admin)
    # check if the user exsist
    if not user:
        raise HTTPException(status_code=404, detail="The user doesn't exists")
    return {"Updated": {"username": username, "isadmin": set_admin}}


@app.delete(
    "/user/{username}",
    responses={
        401: {"detail": "Only admins can perform this function"},
        404: {"detail": "The user doesn't exists"},
        200: {"Deleted": {"username": "name"}},
    },
)
def DeleteUser(
    username: str,
    current_user: schemas.UserRead = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    """
    SQL query: DELETE FROM users WHERE name=name;

    summary: delete user by username (admin function)

    arguments: (username: str), (current_user: schemas.UserRead = Depends(auth.get_current_user)), (db: Session = Depends(get_db))

    return: json message 
    """
    # check for admin
    if not current_user.isadmin:
        raise HTTPException(
            status_code=401, detail="Only admins can perform this function"
        )
    user = crud.delete_user(db=db, username=username)
    # check if the user exsist
    if not user:
        raise HTTPException(status_code=404, detail="The user doesn't exists")
    return {"Deleted": {"username": username}}


# configs


@app.get(
    "/configs",
    responses={
        401: {"detail": "Only admins can perform this function"},
        200: {"Configs": List[schemas.ConfigRead]},
    },
)
def List(
    current_user: schemas.UserRead = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
    owner: str = None,
):
    """
    SQL query: SELECT * FROM configs;
    
    summary: list all configs
    
    arguments: (owner: str [optional (for admins)])
    
    return: valid json contain all configs table rows
    """
    # for admin but not admin
    if (not current_user.isadmin) and owner:
        raise HTTPException(
            status_code=401, detail="Only admins can perform this function"
        )
    # for admin
    elif current_user.isadmin and owner:
        configs = crud.get_configs(db=db, owner=owner)
    elif current_user.isadmin and not owner:
        configs = crud.get_configs(db=db)
    else:
        configs = crud.get_configs(db=db, owner=current_user.username)
    # response
    return {
        "Configs": [
            {
                "owner": config.owner,
                "name": config.name,
                "metadata": config.metadatac,
                "note": config.note,
            }
            for config in configs
        ]
    }


@app.post(
    "/configs",
    responses={
        400: {"detail": "name already exists"},
        200: {"Created": schemas.ConfigCreate},
    },
)
def Create(
    config: schemas.ConfigCreate,
    current_user: schemas.UserRead = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    """
    SQL query: INSERT INTO configs (owner, name, metadata, note) VALUES (ownerValue, nameValue, metadataValue, noteValue)
    
    summary: create new config into configs table

    arguments: (config: ConfigCeate [an instance of ConfigCreate class]), (current_user: schemas.UserRead = Depends(auth.get_current_user))

    return: json response contain success message or failed message with 400 
    """
    # check for exists config
    if crud.get_config(name=config.name, owner=current_user.username, db=db):
        raise HTTPException(status_code=400, detail="name already exists")
    # create new config
    new_config = crud.create_config(config=config, owner=current_user.username, db=db)
    return {
        "Created": {
            "owner": new_config.owner,
            "name": new_config.name,
            "metadata": new_config.metadatac,
            "note": new_config.note,
        }
    }


@app.get(
    "/configs/{name}",
    response_model=schemas.ConfigRead,
    responses={
        401: {"detail": "Only admins can perform this function"},
        404: {"detail": "name doesn't exists"},
    },
)
def Get(
    name: str,
    owner: str = None,
    current_user: schemas.ConfigRead = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    """
    SQL query: SELECT * FROM configs WHERE name=name && owner=owner;

    summary: get config by name

    arguments: (name:str [config name]), (owner: str [for admins])

    return: json response if name exists else failed message with 404
    """
    # for admin but not admin
    if (not current_user.isadmin) and owner:
        raise HTTPException(
            status_code=401, detail="Only admins can perform this function"
        )
    # for admin
    elif current_user.isadmin and owner:
        config = crud.get_config(db=db, name=name, owner=owner)
    else:
        config = crud.get_config(db=db, name=name, owner=current_user.username)
    # check for unexists name
    if not config:
        raise HTTPException(status_code=404, detail="name doesn't exists")
    # convert metadatac to metadata
    return {
        "owner": config.owner,
        "name": config.name,
        "metadata": config.metadatac,
        "note": config.note,
    }


@app.put(
    "/configs/{name}",
    responses={
        401: {"detail": "Only admins can perform this function"},
        404: {"detail": "name doesn't exists"},
        200: {"Updated": schemas.ConfigUpdate},
    },
)
def Update(
    name: str,
    config: schemas.ConfigUpdate,
    current_user: schemas.UserRead = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
    owner: str = None,
):
    """
    SQL query: UPDATE configs SET metadata=metadata WHERE name=name && owner=owner;

    summary: update config by name

    arguments: (name: str [config name]), (owner: str [config owner username (optional for admins)])

    return: json response
    """
    # for admin but not admin
    if (not current_user.isadmin) and owner is not None:
        raise HTTPException(
            status_code=401, detail="Only admins can perform this function"
        )
    # for admin
    elif current_user.isadmin and owner is not None:
        config = crud.update_config(db=db, config=config, name=name, owner=owner)
        resowner = owner
    else:
        config = crud.update_config(
            db=db, config=config, name=name, owner=current_user.username
        )
        resowner = current_user.username
    # check for unexists name
    if not config:
        raise HTTPException(status_code=404, detail="name doesn't exists")
    # response
    return {
        "Update": {
            "owner": resowner,
            "name": config.name,
            "metadata": config.metadatac,
            "note": config.note,
        }
    }


@app.delete(
    "/configs/{name}",
    responses={
        401: {"detail": "Only admins can perform this function"},
        404: {"detail": "name doesn't exists"},
        200: {"Deleted": {"owner": "owner", "name": "name"}},
    },
)
def Delete(
    name: str,
    current_user: schemas.UserRead = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
    owner: str = None,
):
    """
    SQL query: DELETE FROM configs WHERE name=name && owner=owner;

    summary: delete config by name

    arguments: (name: str [config name]), (owner: str [config owner username])

    return: json succeed message if config has deleted else failed message if config doesn't exists
    """
    # for admin but not admin
    if (not current_user.isadmin) and owner is not None:
        raise HTTPException(
            status_code=401, detail="Only admins can perform this function"
        )
    # for admin
    elif current_user.isadmin and owner is not None:
        success = crud.delete_config(db=db, name=name, owner=owner)
        resowner = owner
    else:
        success = crud.delete_config(db=db, name=name, owner=current_user.username)
        resowner = current_user.username
    # check for unexists name
    if not success:
        raise HTTPException(status_code=404, detail="name doesn't exists")
    # response
    return {"Delete": {"owner": resowner, "name": name}}


@app.get(
    "/search/metadata.{key}={value}",
    responses={
        401: {"detail": "Only admins can perform this function"},
        200: {"Configs": [schemas.ConfigBase]},
    },
)
def Query(
    key: str,
    value: str,
    current_user: schemas.UserRead = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
    all: bool = False,
    owner: str = None,
):
    """
    SQL query: SELECT * FROM configs WHERE (configs.metadata #>> %(metadata_1)s) = %(param_1)s;

    summary: get all configs has specific metadata by nested key and value

    arguments: (key: str [nested keys]), (value: str [last key value]), (all: bool = False [optional for admin (search scope)]), (owner: str [optional for admins])

    return: valid json contain all configs matched by metadata search
    """
    # fetch path keys from path params
    keys = key.split(".")
    # for admin but not admin
    if (not current_user.isadmin) and all:
        raise HTTPException(
            status_code=401, detail="Only admins can perform this function"
        )
    elif current_user.isadmin and all:
        configs = crud.query_metadata(db=db, keys=keys, value=value, all=all)
    elif current_user.isadmin and not all and owner:
        configs = crud.query_metadata(
            db=db, keys=keys, value=value, all=all, owner=owner
        )
    else:
        configs = crud.query_metadata(
            db=db, keys=keys, value=value, all=all, owner=current_user.username
        )
    return {
        "Configs": [
            {
                "owner": config.owner,
                "name": config.name,
                "metadata": config.metadatac,
                "note": config.note,
            }
            for config in configs
        ]
    }
