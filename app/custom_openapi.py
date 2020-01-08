import json


def custom_openapi():
    """
    Custom openAPI swagger UI

    Purpose: support Request query param @ [Query : GET : /search]
    """
    from .main import app

    # cache generated schema
    if app.openapi_schema:
        return app.openapi_schema

    # read custom schema
    with open("app/custom_openapi.json", "r") as j:
        openapi_schema = json.loads(j.read())

    # set new schema
    app.openapi_schema = openapi_schema
    return app.openapi_schema
