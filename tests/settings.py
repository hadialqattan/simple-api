from app import crud, database, schemas
from .IO import URLs


def create_users():
    """
    create test users: 

        - username: admin, password: admin, isadmin: "true"
        
        - username: user2, password: user2pass, isadmin: "false"
    """
    if not crud.get_user(
        db=database.SessionLocal(), username="admin"
    ) and not crud.get_admins(db=database.SessionLocal()):
        user = schemas.UserCreate(
            **{"username": "admin", "password": "admin", "isadmin": "true"}
        )
        crud.create_user(db=database.SessionLocal(), user=user)
    if not crud.get_user(db=database.SessionLocal(), username="user2"):
        user = schemas.UserCreate(
            **{"username": "user2", "password": "user2pass", "isadmin": "false"}
        )
        crud.create_user(db=database.SessionLocal(), user=user)


def create_configs():
    """
    create test configs
    """
    # admin default config for testing
    config1 = schemas.ConfigCreate(
        **{
            "owner": "admin",
            "name": "api-1",
            "metadata": {
                "name": "SimpleAPI",
                "url": "http://127.0.0.1:5057",
                "database": {
                    "name": "apidb",
                    "type": "sql",
                    "ms": "postgresql",
                    "host": "0.0.0.0",
                    "port": "5432",
                    "enabled": "true",
                    "running": "true",
                },
                "enabled": "true",
                "running": "true",
            },
            "note": "The api has been enabled.",
        }
    )

    # user2 default config for testing
    config2 = schemas.ConfigCreate(
        **{
            "owner": "user2",
            "name": "api-2",
            "metadata": {
                "name": "SimpleAPI",
                "url": "http://127.0.0.1:5057",
                "database": {
                    "name": "apidb",
                    "type": "sql",
                    "ms": "postgresql",
                    "host": "0.0.0.0",
                    "port": "5432",
                    "enabled": "true",
                    "running": "false",
                },
                "enabled": "true",
                "running": "false",
            },
            "note": "The api has been enabled without the DB!",
        }
    )

    # create admin config
    if not crud.get_config(db=database.SessionLocal(), name="api-1", owner="admin"):
        crud.create_config(db=database.SessionLocal(), config=config1, owner="admin")

    # create user2 config
    if not crud.get_config(db=database.SessionLocal(), name="api-2", owner="user2"):
        crud.create_config(db=database.SessionLocal(), config=config2, owner="user2")
