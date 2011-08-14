# This module should contain all random data to be shared between 
# child parent/child processes created using os.fork.
import tempfile, os
TEMP_DIR = tempfile.mkdtemp()
IPC_SOCKET_DIR = TEMP_DIR
LOG_DIR = TEMP_DIR
PID_DIR = TEMP_DIR
SERVER_STORAGE = False
