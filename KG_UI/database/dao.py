from database.cache import CacheDAO
from database.dto import Path, Node, Edge, Triple
import re

class DAO:
    '''
    This is a base class for implementing database access objects. Any class that talks to the database must implement DAO
    '''

    def execute_query(self,tx,query):
        '''
        This method uses the input transaction object and queries the database. It returns a result list of values.

        Attributes:
        tx : transaction object
        query: cypher query for execution

        Return:
        results -> List : list of values
        '''
        results = list()
        for record in tx.run(query):
            results.extend(record.values())
        return results
    
    
class RelationDAO(DAO):
    '''
    This class extends DAO class and manages all transactions related to relationship data. It could be impact relationships or ontological relations.
    '''

    def __init__(self, db_driver) -> None:
        '''
        This is the initialization method for RelationDAO. It requires the database driver object.
        
        Attributes:
        db_driver: neo4j driver object
        '''
        self.driver = db_driver

    def get_possible_relationships(self) -> list:
        '''
        This method retrieves all impact relationships from the cache data. 
        
        Returns:
        list of impact relationships
        '''
        return CacheDAO.get_impact_relationships(self.driver)

    def query_paths(self,tx,query,hop):
        '''
        This method executes the input query using the transaction object. 
        It maps the returned data to node and edge data transfer objects using the input hop count value.
        
        Attributes:
        tx: transaction object
        query: query for retrieving the paths
        hop: the degree of separation between two nodes

        Returns:
        list of dto.Path
        '''
        paths = list()
        for record in tx.run(query):
            start_node_obj = Node(record['dc_start.id'],record['dc_start.canonical_name'])
            start_node_obj.set_synonyms(record['dc_start.alter_names'])
            nodes = [start_node_obj]
            edges = [(record['r1_type'],record['r1.doc_id'],record['r1.sent_text'],record['r1.doc_id_type'])]
            for i in range(2,hop+1):
                idc_node_name = 'idc{hop}.canonical_name'.format(hop=i-1)
                idc_node_id = 'idc{hop}.id'.format(hop=i-1)
                idc_node_synonyms = 'idc{hop}.alter_names'.format(hop=i-1)
                idc_node_obj = Node(record[idc_node_id],record[idc_node_name])
                idc_node_obj.set_synonyms(record[idc_node_synonyms])
                nodes.append(idc_node_obj)
                edge_type = 'r{hop}_type'.format(hop=i)
                edge_doc_id = 'r{hop}.doc_id'.format(hop=i)
                edge_doc_type = 'r{hop}.doc_id_type'.format(hop=i)
                edge_sent_text = 'r{hop}.sent_text'.format(hop=i)
                edges.append((record[edge_type],record[edge_doc_id],record[edge_sent_text],record[edge_doc_type]))
            end_node_obj = Node(record['dc_end.id'],record['dc_end.canonical_name'])
            end_node_obj.set_synonyms(record['dc_end.alter_names'])
            nodes.append(end_node_obj)
            
            triples_hash_dict = {}
            triples = list()
            for idx,edge_tup in enumerate(edges):
                start_node = nodes[idx]
                end_node = nodes[idx+1]
                edge = Edge(start_node,end_node,edge_tup[0])
                edge.set_pmid(edge_tup[1])
                edge.set_sent_text(edge_tup[2])
                edge.set_doc_type(edge_tup[3])
                hash_triple = hash((start_node.get_node(),edge.get_type(),end_node.get_node()))
                triple = triples_hash_dict.get(hash_triple)
                if not triple:
                    triple = Triple(start_node,edge,end_node)
                    triples_hash_dict[hash_triple] = triple
                triple.include_evidence(edge.get_pmid(),edge.get_sent_text(), edge.get_evidence_link())
                triples.append(triple)
            paths.append(Path(triples))
        return paths    

    def format_display_query(self, query, query_hop, user_hop):
        '''
        This method formats the input query to fetch node and edge data instead of node attributes and edge attributes
        
        Attributes:
        query: the cypher query used for retrieving the impact relationships
        query_hop: the hop value of the current query
        user_hop: the hop value selected by user in the UI

        Returns:
        query : cypher query for display
        '''
        return_pattern = re.compile(r'return.*?')
        return_match = return_pattern.search(query)
        query = query[:return_match.end()+1]
        base_return_query = 'e{hop}, r{hop}, a{hop}'
        base_return_query_NULL = 'NULL as e{hop}, NULL as r{hop}, NULL as a{hop}'
        return_query = 'dc_start, '+base_return_query.format(hop=1)
        for curr_hop in range(1,user_hop):
            if query_hop < user_hop:
                return_query += ', NULL as idc{hop}, '.format(hop=curr_hop)    
                return_query = return_query + base_return_query_NULL.format(hop=curr_hop+1)
            else:                    
                return_query += ', idc{hop}, '.format(hop=curr_hop)
                return_query = return_query + base_return_query.format(hop=curr_hop+1)
        return_query = return_query+', dc_end'
        query = query + return_query
        return query

    def get_ontological_impact_relations(self,start_nodes,end_nodes,rel,hop=1):
        '''
        This method retrieves the impact relationships between two nodes. 
        Depending on the hop value, the query is dynamically generated to retrieve transitive relationships between the two nodes.
        It modifies the type of retrieval to wild card vs absolute based on input.
        If there is no value for start_nodes, a wild card search is performed for that attribute. Similarly for end_nodes as well.
        
        Attributes:
        start_nodes: nodes from where the relationships originate
        end_nodes: nodes at which the relationships end
        rel: type of impact relationships of interest
        hop: degrees of separation (or the transitive path counts between the nodes)

        Returns:
        start_end_paths: list of dto.Path
        display_query: cypher query associated with the retrieval and modified for node level and edge level.
        '''
        start_node_query = 'dc_start.canonical_name {rel_op} {start_nodes}'
        start_node_query = start_node_query.format(start_nodes=start_nodes,rel_op='in') if start_nodes else start_node_query.format(start_nodes="'.*'",rel_op='=~')
        end_node_query = 'dc_end.canonical_name {rel_op} {end_nodes}'
        end_node_query = end_node_query.format(end_nodes=end_nodes,rel_op='in') if end_nodes else end_node_query.format(end_nodes="'.*'",rel_op='=~')

        base_return_query = 'type(r{hop}) as r{hop}_type,r{hop}.doc_id,r{hop}.sent_text,r{hop}.doc_id_type'

        base_path = '''<-[:HAS_CANONICAL_NAME]
                        -(e{hop}:Affector)
                        -[r{hop}:{impact_relations}]
                        -(a{hop}:Affected)
                        -[:HAS_CANONICAL_NAME]->'''        
        base_query = '''MATCH path=(dc_start:DictionaryConcept)
                {path}
                (dc_end:DictionaryConcept)
                where {start_node_query}
                and {end_node_query}
                return distinct dc_start.canonical_name, dc_start.id, dc_start.alter_names, 
                dc_end.canonical_name, dc_end.id, dc_end.alter_names, 
                {return_query}'''
        
        path = return_query = display_query = ''
        start_end_paths = list()
        for curr_hop in range(1,hop+1):
            path += base_path.format(hop=curr_hop,impact_relations=rel)
            return_query += base_return_query.format(hop=curr_hop)
            query = base_query.format(path=path,\
                                      start_node_query=start_node_query,\
                                        end_node_query=end_node_query,\
                                        return_query=return_query)
            with self.driver.session() as session:
                curr_hop_paths = session.execute_read(self.query_paths, query, curr_hop)
                start_end_paths.extend(curr_hop_paths)
            display_query = display_query + self.format_display_query(query, curr_hop, hop) + ' union '            
            path += '(idc{hop}:DictionaryConcept)'.format(hop=curr_hop)
            return_query += ',idc{hop}.canonical_name,idc{hop}.id,idc{hop}.alter_names,'.format(hop=curr_hop)
        display_query = display_query.rstrip(' union ')
        return start_end_paths, display_query



class DictionaryDAO(DAO):
    
    '''
    This class extends DAO class and manages all transactions related specifically to dictionary data.
    '''

    def __init__(self, db_driver) -> None:
        '''
        This method initializes the DictionaryDAO object and requires the database driver
        '''
        self.driver = db_driver
    
    def get_canonical_names(self) -> list:
        '''
        This method returns the unique canonical names of all dictionary concepts.
        '''
        return CacheDAO.get_canonical_names(self.driver)    


class OntologyDAO(DAO):
    
    '''
    This class extends DAO class and manages all transactions related to ontology data.
    '''

    def __init__(self, db_driver) -> None:
        '''
        This method initializes the OntologyDAO and requires the database driver.
        '''
        self.driver = db_driver

    def get_relationships(self) -> list:
        '''
        This method returns all the unique relationships that connects two ontological concepts. 
        '''
        return CacheDAO.get_ontological_relationships(self.driver)
    
    def get_ontology_names(self):
        '''
        This method returns all the names of the ontological concepts.
        '''
        return CacheDAO.get_ontology_names(self.driver)

    def get_sub_ontologies(self, ontology_name, ontology_relations):
        '''
        This method returns the subontologies of a given ontological concept. It requires the onotology name of interest (parent) and all the onotology relations
        '''
        query = "MATCH (oc1:OntologicalConcept)-[r:{relations}*]->(oc2:OntologicalConcept) where oc2.name='{name}' RETURN DISTINCT oc1.name"
        query = query.format(relations=ontology_relations,name=ontology_name)
        with self.driver.session() as session:
            names = session.execute_read(self.execute_query, query)
        return names

    def get_dictionary_canonical_names(self,ontology_names):
        '''
        This method returns the canonical names of dictionary concepts that are subclasses of a given ontology/ontologies.
        '''
        query = 'MATCH (dc:DictionaryConcept)-[r]-(oc:OntologicalConcept) where oc.name in {ontology_names} return distinct(dc.canonical_name)'
        query = query.format(ontology_names=ontology_names)
        with self.driver.session() as session:
            dictionary_canonical_names = session.execute_read(self.execute_query, query)
        return dictionary_canonical_names