import streamlit as st
from service.relation_service import RelationService
from service.dictionary_service import DictionaryService
from service.ontology_service import OntologyService

@st.cache_data
def retrieve_base_values(_dictionary_service, _ontology_service, _relation_service):
    '''
    This method retrieves the values required for initial load of the UI
    It includes the canonical names of all the dictionary concepts.
    It includes the names of all the ontology concepts.
    It includes all the impact relationships.
    '''
    leaf_nodes = _dictionary_service.get_canonical_names()
    class_nodes = _ontology_service.get_ontology_names()
    relations = _relation_service.get_possible_relationships()
    return leaf_nodes, class_nodes, relations

class Controller:

    '''
    This class handles the calls from view to service layer and fetches the results.
    '''

    def __init__(self):
        '''
        Intiantiation of the controller class creates the required service instances.
        '''
        self.dictionary_service = DictionaryService()
        self.ontology_service = OntologyService()
        self.relation_service = RelationService()

    def get_base_values(self):
        '''
        This method fetches the base values for intial load of the screen.
        '''
        return retrieve_base_values(self.dictionary_service,self.ontology_service,self.relation_service)

    def get_subclasses(self,node_class):
        '''
        This method fetches the subclasses of a given ontology class

        Attributes:
        node_class: an ontological node

        Returns:
        list of canonical names of dictionary concepts
        '''
        return self.ontology_service.get_dictionary_canonical_names(node_class)
    
    def get_paths(self,start_nodes, end_nodes, relations, hop_cnt):
        '''
        This method retrieves the paths between two nodes. It matches the input relations and the hop_cnt

        Attributes:
        start_nodes: list of dictionary concepts
        end_nodes: list of dictionary concepts
        relations: list of impact relationships between affector and affected nodes
        hop_cnt: string value denoting the 'Degrees of Separation' value

        Returns:
        list of paths and cypher query
        '''
        return self.relation_service.get_ontological_impact_relations(start_nodes,end_nodes,relations,hop_cnt)


    
    