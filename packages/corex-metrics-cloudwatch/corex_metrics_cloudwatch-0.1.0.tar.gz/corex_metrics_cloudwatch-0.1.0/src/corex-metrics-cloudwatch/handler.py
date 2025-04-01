# Handler for cloudwatch implementing metrics interface
from corex.core.interfaces.metrics import MetricsInterface

class CloudwatchHandler(MetricsInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling metrics with cloudwatch")
