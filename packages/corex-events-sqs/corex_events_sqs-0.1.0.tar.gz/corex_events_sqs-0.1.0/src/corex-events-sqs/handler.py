# Handler for sqs implementing events interface
from corex.core.interfaces.events import EventsInterface

class SqsHandler(EventsInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling events with sqs")
