# This module should contain all random data to be shared between 
# child parent/child processes created using os.fork.
import tempfile
STORAGE_SOCKET_DIR = tempfile.mkdtemp()
