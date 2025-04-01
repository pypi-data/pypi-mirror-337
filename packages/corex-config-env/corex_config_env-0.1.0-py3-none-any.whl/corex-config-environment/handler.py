# Handler for environment implementing config interface
from corex.core.interfaces.config import ConfigInterface

class EnvironmentHandler(ConfigInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling config with environment")
