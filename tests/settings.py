from app import crud, database, schemas
from .IO import URLs


def create_users():
    """
    create test users: 

        - username: admin, password: admin, isadmin: True
        
        - username: user2, password: user2pass, isadmin: False
    """
    if not crud.get_user(
        db=database.SessionLocal(), username="admin"
    ) and not crud.get_admins(db=database.SessionLocal()):
        user = schemas.UserCreate(
            **{"username": "admin", "password": "admin", "isadmin": True}
        )
        crud.create_user(db=database.SessionLocal(), user=user)
    if not crud.get_user(db=database.SessionLocal(), username="user2"):
        user = schemas.UserCreate(
            **{"username": "user2", "password": "user2pass", "isadmin": False}
        )
        crud.create_user(db=database.SessionLocal(), user=user)


def create_configs():
    """
    create test configs
    """
    # admin default config for testing
    config1 = schemas.ConfigCreate(
        **{
            "name": "datacenter-1",
            "metadata": {
                "monitoring": {"enabled": "true"},
                "limits": {"cpu": {"enabled": "false", "value": "300m"}},
            },
            "note": "The cpu has not enabled yet.",
        }
    )

    # user2 default config for testing
    config2 = schemas.ConfigCreate(
        **{
            "name": "datacenter-2",
            "metadata": {
                "monitoring": {"enabled": "true"},
                "limits": {"cpu": {"enabled": "true", "value": "250m"}},
            },
            "note": "The cpu has enabled.",
        }
    )

    # create admin config
    if not crud.get_config(
        db=database.SessionLocal(), name="datacenter-1", owner="admin"
    ):
        crud.create_config(db=database.SessionLocal(), config=config1, owner="admin")

    # create user2 config
    if not crud.get_config(
        db=database.SessionLocal(), name="datacenter-2", owner="user2"
    ):
        crud.create_config(db=database.SessionLocal(), config=config2, owner="user2")
