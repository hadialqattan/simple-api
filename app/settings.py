from fastapi.openapi.utils import get_openapi

# local imports 
from . import crud, schemas, database, main


def create_admin():
    """
    this will work if there's no admin in the DB (username: admin, password: admin)
    """
    try:
        if not crud.get_user(
            db=database.SessionLocal(), username="admin"
        ) and not crud.get_admins(db=database.SessionLocal()):
            user = schemas.UserCreate(
                **{"username": "admin", "password": "admin", "isadmin": True}
            )
            crud.create_user(db=database.SessionLocal(), user=user)
    except Exception as ex:
        print("Cannot create default admin: (there's no admin)")
        print(ex)


def custom_openapi():
    """
    custom openapi 
    """
    # cache openapi
    if main.app.openapi_schema: 
        return main.app.openapi_schema
    # get the schema
    openapi_schema = get_openapi(
        title="SimpleAPI",
        version="2.0.0",
        description="SimpleAPI is a restful API provids simple service that stores and returns configurations with simple jwt authentication using FastAPI and PostgreSQL. <a href='https://github.com/HadiZakiAlQattan/simpleapi/blob/master/README.md'>Full documentation</a>",
        routes=main.app.routes
    )
    main.app.openapi_schema = openapi_schema
    return main.app.openapi_schema
