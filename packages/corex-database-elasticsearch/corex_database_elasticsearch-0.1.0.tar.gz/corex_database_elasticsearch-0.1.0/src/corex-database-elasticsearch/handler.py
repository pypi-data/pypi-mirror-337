# Handler for elasticsearch implementing database interface
from corex.core.interfaces.database import DatabaseInterface

class ElasticsearchHandler(DatabaseInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling database with elasticsearch")
