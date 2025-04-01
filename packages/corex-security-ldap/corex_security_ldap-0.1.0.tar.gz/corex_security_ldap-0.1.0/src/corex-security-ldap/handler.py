# Handler for ldap implementing security interface
from corex.core.interfaces.security import SecurityInterface

class LdapHandler(SecurityInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling security with ldap")
