#!/usr/bin/env python
import env
import app_config
from migrate.versioning.shell import main
main(url=app_config.DATABASE_CONNECTION_STRING, debug='False', repository='./db_migrations')
