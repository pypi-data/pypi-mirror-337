# Handler for memcached implementing cache interface
from corex.core.interfaces.cache import CacheInterface

class MemcachedHandler(CacheInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling cache with memcached")
