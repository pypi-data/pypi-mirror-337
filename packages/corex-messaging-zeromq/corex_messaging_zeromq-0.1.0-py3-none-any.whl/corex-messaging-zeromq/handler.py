# Handler for zeromq implementing messaging interface
from corex.core.interfaces.messaging import MessagingInterface

class ZeromqHandler(MessagingInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling messaging with zeromq")
