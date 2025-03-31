# Handler for loki implementing logging interface
from corex.core.interfaces.logging import LoggingInterface

class LokiHandler(LoggingInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling logging with loki")
