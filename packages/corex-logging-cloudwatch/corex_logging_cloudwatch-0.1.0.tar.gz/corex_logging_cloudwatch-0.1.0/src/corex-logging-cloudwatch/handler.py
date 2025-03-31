# Handler for cloudwatch implementing logging interface
from corex.core.interfaces.logging import LoggingInterface

class CloudwatchHandler(LoggingInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling logging with cloudwatch")
