import mappings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app_config import DATABASE_CONNECTION_STRING, OUTPUT_SQL

SQLALCHEMY_ENGINE = create_engine(DATABASE_CONNECTION_STRING, echo=OUTPUT_SQL)
Session = scoped_session(sessionmaker(SQLALCHEMY_ENGINE))
