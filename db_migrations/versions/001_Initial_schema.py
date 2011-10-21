from sqlalchemy import *
from migrate import *
from database.tables import metadata as kgenie_metadata


def upgrade(migrate_engine):
    kgenie_metadata.create_all(migrate_engine)

def downgrade(migrate_engine):
    kgenie_metadata.drop_all(migrate_engine)
