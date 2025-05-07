import streamlit as st
from database.access import DatabaseAccess

class CacheDAO:

    '''
    This class caches the data that are retrieved from database in the initial load.
    '''

    def execute_query(tx, query):
        '''
        This method executes the query using the input transaction object and returns a list of the results

        Attributes:
        tx: transaction object
        query: cypher query

        Returns:
        result -> list: list of values
        '''
        results = list()
        for record in tx.run(query):
            results.extend(record.values())
        return results
    
    def query_book_node(tx, query):
        '''
        This method executes the query using the input transaction object and returns a dict of the results. 
        This method should be used to retrieve the metadata of the book nodes.

        Attributes:
        tx: transaction object
        query: cypher query

        Returns:
        result -> dict: dictionary of isbn (book unique identifier) and the URL to identify the book.
        '''
        book_link_map = dict()
        for record in tx.run(query):
            book_link_map[record['isbn']] = record['link']
        return book_link_map
    
    def query_dictionary_nodes(tx, query):
        '''
        This method executes the query using the input transaction object and returns a set start nodes and end nodes.
        This method is used to retrieve canonical names of start nodes and end nodes

        Attributes:
        tx: transaction object
        query: cypher query

        Returns:
        result -> set:start nodes, set:end nodes
        '''
        start_nodes = set()
        end_nodes = set()
        for record in tx.run(query):
            start_nodes.add(record['start_nodes'])
            end_nodes.add(record['end_nodes'])
        return start_nodes, end_nodes

    @st.cache_data
    def get_canonical_names(_db_driver) -> list:
        '''
        This method retrieves the unique canonical names of dictionary concepts for start and end nodes. It caches this data.

        Attributes:
        _db_driver: database driver object

        Returns:
        canonical_names -> list: list of canonical names
        '''
        query = """
                match (dc_start:DictionaryConcept)
                    <-[:HAS_CANONICAL_NAME]
                    -(e1:Affector)
                    -[r1:CORRELATED_NOT_SPECIFIED|POSITIVELY_CORRELATED|NEGATIVELY_CORRELATED|NOT_CORRELATED]
                    -(a1:Affected)
                    -[:HAS_CANONICAL_NAME]->
                    (dc_end:DictionaryConcept)  
                    return dc_start.canonical_name as start_nodes, 
                    dc_end.canonical_name as end_nodes
                """
        with _db_driver.session() as session:
            start_nodes, end_nodes = session.execute_read(CacheDAO.query_dictionary_nodes, query)
        return start_nodes, end_nodes
    
    @st.cache_data
    def get_ontological_relationships(_db_driver) -> list:
        '''
        This method retrieves the unique ontological relationships and returns the list. It caches this data.

        Attributes:
        _db_driver: database driver object

        Returns:
        relations -> list: list of ontological relationships
        '''
        query = 'MATCH(n1:DictionaryConcept|OntologicalConcept)-[r]-(n2:OntologicalConcept) RETURN DISTINCT(type(r))'
        with _db_driver.session() as session:
            relations = session.execute_read(CacheDAO.execute_query, query)
        return relations

    # @st.cache_data
    # def get_ontology_names(_db_driver) -> list:
    #     '''
    #     This method retrieves the unique ontology names and returns the list. It caches this data.

    #     Attributes:
    #     _db_driver: database driver object

    #     Returns:
    #     ontology_names -> list: list of ontology names
    #     '''
    #     query = 'MATCH(oc:OntologicalConcept) return DISTINCT(oc.name)'
    #     with _db_driver.session() as session:
    #         ontology_names = session.execute_read(CacheDAO.execute_query, query)
    #     return ontology_names
    
    @st.cache_data
    def get_ontology_start_classes(_db_driver) -> list:
        '''
        This method retrieves the unique ontology names of those start classes that have at least one impact relationship 
        and returns the list. It caches this data.

        Attributes:
        _db_driver: database driver object

        Returns:
        ontology_names -> list: list of ontology names
        '''
        query = """
                match (onto:OntologicalConcept)<-[*1..5]-(dc:DictionaryConcept)
                    <-[:HAS_CANONICAL_NAME]
                    -(e1:Affector)
                    -[r1:CORRELATED_NOT_SPECIFIED|POSITIVELY_CORRELATED|NEGATIVELY_CORRELATED|NOT_CORRELATED]
                    ->(a1:Affected) 
                return distinct(onto.name);
                """
        with _db_driver.session() as session:
            start_classe_names = session.execute_read(CacheDAO.execute_query, query)
        return start_classe_names
    
    @st.cache_data
    def get_ontology_end_classes(_db_driver) -> list:
        '''
        This method retrieves the unique ontology names of those end classes that have at least one impact relationship 
        and returns the list. It caches this data.

        Attributes:
        _db_driver: database driver object

        Returns:
        ontology_names -> list: list of ontology names
        '''
        query = """
                match (onto:OntologicalConcept)<-[*1..5]-(dc:DictionaryConcept)
                    <-[:HAS_CANONICAL_NAME]
                    -(a1:Affected)
                    <-[r1:CORRELATED_NOT_SPECIFIED|POSITIVELY_CORRELATED|NEGATIVELY_CORRELATED|NOT_CORRELATED]
                    -(e1:Affector) 
                return distinct(onto.name);
                """
        with _db_driver.session() as session:
            end_classe_names = session.execute_read(CacheDAO.execute_query, query)
        return end_classe_names
    
    @st.cache_data
    def get_impact_relationships(_db_driver) -> list:
        '''
        This method retrieves the unique impact relationships and returns the list. It caches this data.

        Attributes:
        _db_driver: database driver object

        Returns:
        impact_relations -> list: list of impact relationships
        '''
        query = "MATCH (e:Affector)-[r]-(a:Affected) RETURN DISTINCT type(r)"
        with _db_driver.session() as session:
            impact_relations = session.execute_read(CacheDAO.execute_query, query)
        return impact_relations

    @st.cache_data
    def get_book_metadata(_db_driver) -> list:
        '''
        This method retrieves the metadata of the book chapter nodes. It currently retrieves isbn and link of the book nodes.
        It caches this data.

        Attributes:
        _db_driver: database driver object

        Returns:
        book_metadata -> dict: dictionary of isbn and its link
        '''
        query = "MATCH (n:BookChapter) RETURN distinct n.isbn as isbn, n.link as link"
        with _db_driver.session() as session:
            book_metadata = session.execute_read(CacheDAO.query_book_node, query)
        return book_metadata
    
class CacheData:
    '''
    This class hosts the methods that cache data via lazy load. They are not required for initial load but retrieved through the application cycle.
    '''
    def get_book_metadata(doc_id):
         books_metadata = CacheDAO.get_book_metadata(DatabaseAccess.get_driver())
         return books_metadata.get(doc_id)