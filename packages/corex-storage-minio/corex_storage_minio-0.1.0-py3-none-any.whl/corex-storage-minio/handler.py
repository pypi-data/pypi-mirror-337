# Handler for minio implementing storage interface
from corex.core.interfaces.storage import StorageInterface

class MinioHandler(StorageInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling storage with minio")
