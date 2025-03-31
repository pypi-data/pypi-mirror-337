# Handler for mysql implementing database interface
from corex.core.interfaces.database import DatabaseInterface

class MysqlHandler(DatabaseInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling database with mysql")
