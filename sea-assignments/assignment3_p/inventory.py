import hashlib
import getpass

NUM_INDEX_SHARDS = 3
NUM_DOC_SHARDS = 3
MAX_PORT = 49152
MIN_PORT = 10000
BASE_PORT = int(hashlib.md5(getpass.getuser()).hexdigest()[:8], 16) % \
  (MAX_PORT - MIN_PORT) + MIN_PORT
# BASE_PORT = 40010
servers = {}
servers['web'] = ["127.0.0.1:%d" % (BASE_PORT)]
servers['index'] = ["127.0.0.1:%d" % (port) 
  for port in range(BASE_PORT + 1, 
                    BASE_PORT + 1 + NUM_INDEX_SHARDS)]
servers['doc'] = ["127.0.0.1:%d" % (port) 
  for port in range(BASE_PORT + 1 + NUM_INDEX_SHARDS, 
                    BASE_PORT + 1 + NUM_INDEX_SHARDS + NUM_DOC_SHARDS)]

  
