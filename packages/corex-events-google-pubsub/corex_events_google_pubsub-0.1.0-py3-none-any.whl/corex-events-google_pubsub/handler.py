# Handler for google_pubsub implementing events interface
from corex.core.interfaces.events import EventsInterface

class Google_pubsubHandler(EventsInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling events with google_pubsub")
