"""
CRUD comes from: Create, Read, Update, and Delete.
"""

from sqlalchemy.orm import Session

# local import
from . import models, schemas, auth


def get_users(db: Session):
    """
    desined for [ListUsers : GET : /users] endpoint

    SQL query: SELECT * FROM users;

    summary: get all users (this function used by admins)

    arguments: (db: Session [sqlalchemy database session])

    return: list of users: List[User]
    """
    return db.query(models.User).all()


def get_admins(db: Session):
    """
    desined for [GetAdmins : GET : /users/admins]

    SQL query: SELECT * FROM users WHERE isadmin=true;

    summary get all admins

    arguments: (db: Session [sqlalchemy database session])

    return: admins list
    """
    return db.query(models.User).filter(models.User.isadmin == True).all()


def create_user(db: Session, user: schemas.UserCreate):
    """
    desined for [CreateUser : POST : /user] endpoint

    SQL query: INSERT INTO users (id, pubilc_id, name, password, isadmin) VALUES (idValue, public_idValue, nameValue, passwordValue, isadminValue);

    summary: insert new user into users table

    arguments: (db: Session [sqlalchemy database session]), (user: schemas.UserCreate [instance of UserCreate model])

    return: new user
    """
    db_user = models.User(
        username=user.username,
        password=auth.get_password_hash(user.password),
        isadmin=user.isadmin,
        configs=[],
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, username: str):
    """
    desined for [GetUser : GET : /user/{username}] endpoint

    SQL query: SELECT * FROM users WHERE username=username;

    summary: get user by name

    arguments: (db: Session [sqlalchemy database session]), (username: str)

    return: user
    """
    return db.query(models.User).filter(models.User.username == username).first()


def update_user(db: Session, username: str, isadmin: bool):
    """
    desined for [UpdateUser : PUT : /user/{username}/{isadmin}] endpoint

    SQL query: UPDATE users SET isadmin=isadmin WHERE username=username;

    summary: update user admin permission

    arguments: (db: Session [sqlalchemy database session]), (username: str), (isadmin: bool)

    return: updated user
    """
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        return False
    db_user.isadmin = isadmin
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, username: str):
    """
    desined for [DeleteUser : DELETE : /user/{username}] endpoint

    SQL query: DELETE FROM configs WHERE name=name;

    summary: update user admin permission

    arguments: (db: Session [sqlalchemy database session]), (username: str)

    return: True if user has been deleted otherwise False
    """
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True


def get_configs(db: Session, owner: str = None):
    """
    designed for [List : GET : /configs] endpoint

    SQL query: SELECT * FROM configs;

    summary: list all configs

    arguments: (db: Session [sqlalchemy database session]) (owner: str [owner username (scope)])

    return: all configs table rows
    """
    if owner is None:
        return db.query(models.Config).all()
    else:
        return db.query(models.Config).filter(models.Config.owner == owner).all()


def get_configs_by_username(db: Session, username: str):
    """
    designed for [User : GET : /configs/{username}] endpoint

    SQL query: SELECT * FROM configs WHERE user_id=user_id;

    summary: get config by username

    arguments: (db: Session [sqlalchemy database session]), (username: str [owner username])

    return: config or False
    """
    # get user_id from username
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        return False
    user_id = db_user.id
    # get the config by the user_id
    db_config = db.query(models.Config).filter(models.Config.user_id == user_id).first()
    if not db_config:
        return False
    return db_config


def create_config(db: Session, config: schemas.ConfigCreate, owner: str):
    """
    designed for [Create : POST : /configs]

    SQL query: INSERT INTO configs (owner, name, metadatac, note) VALUES (ownerValue, nameValue, metadatacValue, noteValue);

    summary: create new config into configs table

    arguments: (db: Session [sqlalchemy database session]), (config: schemas.ConfigCeate [an instance of schemas.Config class]), (owner: str)

    return: new config
    """
    db_config = models.Config(
        owner=owner, name=config.name, metadatac=dict(config.metadata), note=config.note
    )
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config


def get_config(db: Session, name: str, owner: str):
    """
    designed for [GET : GET : /configs/{name}] endpoint

    SQL query: SELECT * FROM configs WHERE name=name && owner=owner;

    summary: get config by name

    arguments: (db: Session [sqlalchemy database session]), (name: str [config name]), (owner: str [owner username])

    return: single config
    """
    return (
        db.query(models.Config)
        .filter(models.Config.name == name and models.Config.owner == owner)
        .first()
    )


def update_config(db: Session, config: schemas.ConfigUpdate, name: str, owner: str):
    """
    designed for [Update : PUT : /configs/{name}] endpoint

    SQL query: UPDATE configs SET metadata=metadata WHERE name=name;

    summary: update config by name

    arguments: (db: Session [sqlalchemy database session]), (config: schemas.ConfigUpdate [an instance of ConfigUpdate class]), (name: str [config name]), (owner: str [config owner username])

    return: updated config or false if config doesn't exists
    """
    db_config = (
        db.query(models.Config)
        .filter(models.Config.name == name and models.Config.owner == owner)
        .first()
    )
    if not db_config:
        return False
    db_config.metadatac = config.metadata
    db_config.note = config.note
    db.commit()
    db.refresh(db_config)
    return db_config


def delete_config(db: Session, name: str, owner: str):
    """
    designed for [Delete : DELETE : /configs/{name}]

    SQL query: DELETE FROM configs WHERE name=name;

    summary: delete config by name

    arguments: (db: Session [sqlalchemy database session]), (name: str [config name]), (username: str [owner username])

    return: True if config exits else False
    """
    db_config = (
        db.query(models.Config)
        .filter(models.Config.name == name and models.Config.owner == owner)
        .first()
    )
    if not db_config:
        return False
    db.delete(db_config)
    db.commit()
    return True


def query_metadata(db: Session, keys: list, value: str, all: bool, owner: str = None):
    """
    designed for [Query : GET : /search]

    SQL query: SELECT * FROM configs WHERE (configs.metadata #>> %(metadata_1)s) = %(param_1)s;

    summary: get all configs has specific metadata by keys and value

    arguments: (db: Session [sqlalchemy database session]), (keys: list [list of keys and value]), (owner: str [owner username]), (all: bool [search scope])

    return: List of configs
    """
    if all:
        return (
            db.query(models.Config)
            .filter(models.Config.metadatac[keys].astext == value)
            .all()
        )
    else:
        return (
            db.query(models.Config)
            .filter(
                models.Config.owner == owner
                and models.Config.metadatac[keys].astext == value
            )
            .all()
        )
