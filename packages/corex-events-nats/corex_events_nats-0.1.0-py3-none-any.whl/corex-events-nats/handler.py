# Handler for nats implementing events interface
from corex.core.interfaces.events import EventsInterface

class NatsHandler(EventsInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling events with nats")
