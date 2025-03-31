# Handler for couchbase implementing cache interface
from corex.core.interfaces.cache import CacheInterface

class CouchbaseHandler(CacheInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling cache with couchbase")
