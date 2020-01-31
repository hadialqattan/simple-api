from . import crud, schemas, database


def create_admin():
    """
    this will work if there's no admin in the DB (username: admin, password: admin)
    """
    try:
        if not crud.get_user(
            db=database.SessionLocal(), username="admin"
        ) and not crud.get_admins(db=database.SessionLocal()):
            user = schemas.UserCreate(**{
                "username":"admin", 
                "password":"admin", 
                "isadmin": True
            })
            crud.create_user(db=database.SessionLocal(), user=user)
    except Exception as ex:
        print("Cannot create default admin: (there's no admin)")
        print(ex)
