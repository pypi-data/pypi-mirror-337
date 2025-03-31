# Handler for sns implementing events interface
from corex.core.interfaces.events import EventsInterface

class SnsHandler(EventsInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling events with sns")
