from sqlalchemy import create_engine
from sqlalchemy.sql import text

# database URL and engine
SQLALCHEMY_DATABASE_URL = "postgresql://api_owner:api112233@localhost/apidb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# clean the db
with engine.connect() as con:

    statement = text("""DELETE FROM configs;""")
    con.execute(statement)
