# Handler for auth0 implementing security interface
from corex.core.interfaces.security import SecurityInterface

class Auth0Handler(SecurityInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling security with auth0")
