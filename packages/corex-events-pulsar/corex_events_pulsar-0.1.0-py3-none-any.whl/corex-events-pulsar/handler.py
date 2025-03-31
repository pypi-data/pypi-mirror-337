# Handler for pulsar implementing events interface
from corex.core.interfaces.events import EventsInterface

class PulsarHandler(EventsInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling events with pulsar")
