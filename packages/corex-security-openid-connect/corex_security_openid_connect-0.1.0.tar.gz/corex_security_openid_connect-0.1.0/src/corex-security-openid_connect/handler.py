# Handler for openid_connect implementing security interface
from corex.core.interfaces.security import SecurityInterface

class Openid_connectHandler(SecurityInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling security with openid_connect")
