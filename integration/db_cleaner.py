from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os

# database URL and engine
SQLALCHEMY_DATABASE_URL = (
    "postgresql://"
    + os.environ["DB_OWNER"]
    + ":"
    + os.environ["DB_PASSWORD"]
    + "@"
    + os.environ["HnP"]
    + "/"
    + os.environ["DB"]
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# clean the db
with engine.connect() as con:

    statement = text("""DELETE FROM configs;""")
    con.execute(statement)
