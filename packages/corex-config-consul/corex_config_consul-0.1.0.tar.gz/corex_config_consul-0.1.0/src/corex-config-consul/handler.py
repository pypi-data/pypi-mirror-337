# Handler for consul implementing config interface
from corex.core.interfaces.config import ConfigInterface

class ConsulHandler(ConfigInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling config with consul")
