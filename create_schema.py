#!/usr/bin/env python
import env
from database.tables import metadata
from database.sqlalch import SQLALCHEMY_ENGINE

metadata.create_all(SQLALCHEMY_ENGINE)
