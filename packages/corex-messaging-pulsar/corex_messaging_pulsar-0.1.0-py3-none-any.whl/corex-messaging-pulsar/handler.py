# Handler for pulsar implementing messaging interface
from corex.core.interfaces.messaging import MessagingInterface

class PulsarHandler(MessagingInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling messaging with pulsar")
