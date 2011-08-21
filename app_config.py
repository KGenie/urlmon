# needed for SQLITE db since the daemons run with '/' as cwd
from app_globals import APP_ROOT

# Database
OUTPUT_SQL = False
DATABASE_CONNECTION_STRING = 'sqlite:///%s/umon.db3' % APP_ROOT


# Task daemon
INTERVAL_BETWEEN_TASK_CHECKS = 60
NUMBER_OF_TASK_RUNNERS = 5
