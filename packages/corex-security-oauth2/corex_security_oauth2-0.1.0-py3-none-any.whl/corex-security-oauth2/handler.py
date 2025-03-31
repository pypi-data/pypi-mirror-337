# Handler for oauth2 implementing security interface
from corex.core.interfaces.security import SecurityInterface

class Oauth2Handler(SecurityInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling security with oauth2")
