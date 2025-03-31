# Handler for aerospike implementing cache interface
from corex.core.interfaces.cache import CacheInterface

class AerospikeHandler(CacheInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling cache with aerospike")
