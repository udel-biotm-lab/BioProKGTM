from database.access import DatabaseAccess
from database.dao import RelationDAO

class RelationService:
    '''
    This service class serves to maintain all methods pertaining to Relationship data. 
    It talks to the RelationDAO to retrieves impact relationship information.
    '''

    def __init__(self):
        '''
        This method intializes the RelationSerivce class. 
        It gets the database driver and creates an RelationDAO object.
        '''
        self.dao = RelationDAO(DatabaseAccess.get_driver())
        self.impact_relations = list(self.dao.get_possible_relationships())
    
    def get_possible_relationships(self):
        '''
        This method returns the impact relationships between any two dictionary concepts.
        '''
        return self.impact_relations
    
    def get_impact_relationships(self,start_node,end_node,rel,hop):
        '''
        This method returns the path between two given nodes (the start node and end node). 
        '''
        if not rel: 
            rel = self.get_possible_relationships()
        paths = self.dao.get_impact_relations(start_node,end_node,rel,hop)
        return paths
    
    def get_ontological_impact_relations(self, start_nodes, end_nodes, rel, hop):
        '''
        This method returns the path between two given nodes (the start node and end node). 
        If any of the input node is an ontology, it retrieves all the base dictionary nodes for the ontology and then fetches the impact relationships.
        '''
        if not rel: 
            rel = self.get_possible_relationships()
        rel = '|'.join(rel)
        paths, query = self.dao.get_ontological_impact_relations(start_nodes, end_nodes, rel, hop)
        return paths, query
