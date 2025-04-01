# Handler for activemq implementing messaging interface
from corex.core.interfaces.messaging import MessagingInterface

class ActivemqHandler(MessagingInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling messaging with activemq")
