from database.access import DatabaseAccess
from database.dao import OntologyDAO

class OntologyService:
    '''
    This service class serves to maintain all methods pertaining to Ontology data. 
    It talks to the OntologyDAO to retrieve ontology relation information.
    '''

    def __init__(self):
        '''
        This method intializes the OntologySerivce class. 
        It gets the database driver and creates an OntologyDAO object.
        '''
        self.dao = OntologyDAO(DatabaseAccess.get_driver())
        self.relations = None

    def get_relationships(self):
        '''
        This method retrieves all relationships pertaining to the ontology nodes, and returns a list of the relationships.
        '''
        if not self.relations:
            self.relations = list(self.dao.get_relationships())
        return self.relations
    
    def get_ontology_names(self):
        '''
        This method retrieves all the names of the ontology nodes, and returns a list of the ontology nodes.
        '''
        self.ontology_names = list(self.dao.get_ontology_names())
        return self.ontology_names
    
    def get_dictionary_canonical_names(self,ontology_name):
        '''
        This method retrieves the canonical names of all the dictionary concepts under the ontology_name of interest, and return the list of canonical names.
        '''
        ontology_relations = '|'.join(x for x in self.get_relationships())
        ontologies = [ontology_name]
        ontologies.extend(self.dao.get_sub_ontologies(ontology_name,ontology_relations))
        canonical_names = self.dao.get_dictionary_canonical_names(ontologies)   
        return canonical_names