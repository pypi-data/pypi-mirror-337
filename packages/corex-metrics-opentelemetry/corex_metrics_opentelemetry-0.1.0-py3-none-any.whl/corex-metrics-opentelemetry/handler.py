# Handler for opentelemetry implementing metrics interface
from corex.core.interfaces.metrics import MetricsInterface

class OpentelemetryHandler(MetricsInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling metrics with opentelemetry")
