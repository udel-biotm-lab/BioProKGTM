from database.access import DatabaseAccess
from database.dao import DictionaryDAO

class DictionaryService:

    '''
    This service class serves to maintain all methods pertaining to Dictionary Concept node. 
    It talks to the DictionaryDAO to retrieve Dictionary relation information.
    '''

    def __init__(self):
        '''
        This method intializes the DictionaryService class. 
        It gets the database driver and creates an DictionaryDAO object.
        '''
        self.dao = DictionaryDAO(DatabaseAccess.get_driver())

    def get_canonical_names(self):
        '''
        This method returns the canonical names of the dictionary concepts.
        '''
        return list(self.dao.get_canonical_names())