# Handler for redis implementing cache interface
from corex.core.interfaces.cache import CacheInterface

class RedisHandler(CacheInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling cache with redis")
