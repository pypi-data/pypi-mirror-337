# Handler for hazelcast implementing cache interface
from corex.core.interfaces.cache import CacheInterface

class HazelcastHandler(CacheInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling cache with hazelcast")
