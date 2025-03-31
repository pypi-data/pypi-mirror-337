# Handler for graylog implementing logging interface
from corex.core.interfaces.logging import LoggingInterface

class GraylogHandler(LoggingInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling logging with graylog")
