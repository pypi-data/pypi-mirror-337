# Handler for azure_blob implementing storage interface
from corex.core.interfaces.storage import StorageInterface

class Azure_blobHandler(StorageInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling storage with azure_blob")
