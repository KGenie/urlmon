import mappings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app_config import DATABASE_CONNECTION_STRING, OUTPUT_SQL

listeners = []
## SQLITE Specific to force FK constraints from:
# http://stackoverflow.com/questions/2614984/sqlite-sqlalchemy-how-to-enforce-foreign-keys
if 'sqlite' in DATABASE_CONNECTION_STRING:
    from sqlalchemy.interfaces import PoolListener
    class ForeignKeysListener(PoolListener):
        def connect(self, dbapi_con, con_record):
            db_cursor = dbapi_con.execute('pragma foreign_keys=ON')
    listeners.append(ForeignKeysListener())
##

SQLALCHEMY_ENGINE = create_engine(DATABASE_CONNECTION_STRING, echo=OUTPUT_SQL,
        listeners=listeners)
Session = scoped_session(sessionmaker(SQLALCHEMY_ENGINE))
