from neo4j import GraphDatabase
import os

class DatabaseAccess:

    '''
    This class establishes connection to the database and provides a driver instance.
    '''
    neo4j_driver = None

    @classmethod
    def get_driver(cls):
        '''
        This method creates a new database driver and verifies connectivity, if one doesn't exist. Else, it returns the existing driver object.
        '''
        if cls.neo4j_driver is None:
            cls.neo4j_driver = GraphDatabase.driver(os.getenv("DB_URI"), 
                                                    auth=(os.getenv("DB_USER"),os.getenv("DB_PWD")), 
                                                    database=os.getenv("DB_NAME"))
            cls.neo4j_driver.verify_connectivity()
        return cls.neo4j_driver
    
    @classmethod
    def close_driver(cls):
        '''
        This method closes the existing driver object
        '''
        if cls.neo4j_driver:
            cls.neo4j_driver.close()
            cls.neo4j_driver = None
