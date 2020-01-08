from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os

# database URL and engine
SQLALCHEMY_DATABASE_URL = os.environ["DB_URL"]
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# clean the db
with engine.connect() as con:

    statement = text("""DELETE FROM configs;""")
    con.execute(statement)
