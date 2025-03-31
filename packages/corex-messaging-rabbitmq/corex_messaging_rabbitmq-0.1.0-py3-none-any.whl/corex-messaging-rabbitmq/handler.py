# Handler for rabbitmq implementing messaging interface
from corex.core.interfaces.messaging import MessagingInterface

class RabbitmqHandler(MessagingInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling messaging with rabbitmq")
