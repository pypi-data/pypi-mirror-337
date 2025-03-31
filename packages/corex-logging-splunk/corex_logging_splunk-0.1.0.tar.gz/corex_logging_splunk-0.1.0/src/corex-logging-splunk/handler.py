# Handler for splunk implementing logging interface
from corex.core.interfaces.logging import LoggingInterface

class SplunkHandler(LoggingInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling logging with splunk")
