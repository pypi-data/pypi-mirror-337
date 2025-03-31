# Handler for ignite implementing cache interface
from corex.core.interfaces.cache import CacheInterface

class IgniteHandler(CacheInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling cache with ignite")
