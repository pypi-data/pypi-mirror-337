# Handler for graphite implementing metrics interface
from corex.core.interfaces.metrics import MetricsInterface

class GraphiteHandler(MetricsInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling metrics with graphite")
