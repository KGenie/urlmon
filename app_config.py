# needed for SQLITE db since the daemons run with '/' as cwd
from app_globals import APP_ROOT
from logging import NOTSET, DEBUG, ERROR, WARNING

# Database
OUTPUT_SQL = False
DATABASE_CONNECTION_STRING = 'sqlite:///%s/umon.db' % APP_ROOT


# Task daemon
INTERVAL_BETWEEN_TASK_CHECKS = 10
NUMBER_OF_TASK_RUNNERS = 5

# Logging
LEVELS = {
        'htmldiff': DEBUG,
        'dispatcher': ERROR,
        'daemons': WARNING,
        'daemons.task': DEBUG,
        'services': DEBUG,
        'controllers': DEBUG
        }
