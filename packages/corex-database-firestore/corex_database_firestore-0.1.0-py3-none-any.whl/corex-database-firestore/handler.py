# Handler for firestore implementing database interface
from corex.core.interfaces.database import DatabaseInterface

class FirestoreHandler(DatabaseInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling database with firestore")
