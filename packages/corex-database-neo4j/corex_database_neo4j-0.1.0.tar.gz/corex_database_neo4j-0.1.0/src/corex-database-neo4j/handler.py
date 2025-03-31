# Handler for neo4j implementing database interface
from corex.core.interfaces.database import DatabaseInterface

class Neo4jHandler(DatabaseInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling database with neo4j")
