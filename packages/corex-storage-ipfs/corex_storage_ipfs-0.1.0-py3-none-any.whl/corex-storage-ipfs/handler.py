# Handler for ipfs implementing storage interface
from corex.core.interfaces.storage import StorageInterface

class IpfsHandler(StorageInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling storage with ipfs")
