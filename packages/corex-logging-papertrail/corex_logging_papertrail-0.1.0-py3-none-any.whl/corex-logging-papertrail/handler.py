# Handler for papertrail implementing logging interface
from corex.core.interfaces.logging import LoggingInterface

class PapertrailHandler(LoggingInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling logging with papertrail")
