from collections import defaultdict
import hashlib
import getpass

NUM_WORKERS = 4
MAX_PORT = 49152
MIN_PORT = 10000
BASE_PORT = int(hashlib.md5(getpass.getuser() + "salt").hexdigest()[:8], 16) % \
  (MAX_PORT - MIN_PORT) + MIN_PORT

servers = {}
servers['worker'] = ["127.0.0.1:%d" % (port) 
  for port in range(BASE_PORT, BASE_PORT + NUM_WORKERS)]

  