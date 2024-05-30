from database.cache import CacheData

class Path:
    '''
    This class transfers data about path information between two nodes. It include evidence of the information at triple level. 
    '''
    
    def __init__(self, triples):
        '''
        This method initializes the class and needs the list of triples make the path. 
        It constructs the final route of the path from the input triples. 
        
        Attributes:
        triples: list of triples that make the path
        '''
        self.path_triples = triples
        self._set_final_route()

    def _set_final_route(self):
        '''
        This method constructs the final path from the list of triples.

        '''
        self.route = ''
        self.path_pmid_evidence = []
        self.path_sent_text_evidence = []
        self.path_evidence_link = []
        self.path_nodes = set()

        # This is the base pattern for a triple path
        base_sub_route = '{head}--{rel}({pmids})-->{tail}'
        sub_route = base_sub_route

        # For each triple in the triples, the base pattern is updated to replace the respective nodes and edge, along with evidence 
        for triple in self.path_triples:
            head_tup, tail_tup, rel_type = triple.get_triple(detailed=True)
            pmid_evidence, sent_text_evidence, evidence_link = triple.get_evidence()
            self.path_pmid_evidence.extend(pmid_evidence)
            self.path_sent_text_evidence.extend(sent_text_evidence)
            self.path_evidence_link.extend(evidence_link)
            pmids = ','.join(pmid_evidence)
            self.route += sub_route.format(head=head_tup[1],rel=rel_type,tail=tail_tup[1],pmids=pmids)
            self.path_nodes.add(head_tup[1])
            self.path_nodes.add(tail_tup[1])
            sub_route = ' || '+base_sub_route
    
    def get_path_nodes(self):
        '''
        This method returns the unique nodes (set of nodes) in the path

        Returns
        self.path_nodes : a list of dto.node
        
        '''
        return self.path_nodes

    def get_final_route(self):
        '''
        This method returns the complete route of the path object.

        Return
        self.route : string
        
        '''
        return self.route

    def get_path_evidence(self):
        '''
        This method populates the evidence for every triple path and returns the unique list of evidence associated with the path.

        Return
        unique_pmid_sent_list : set of PMIDs (string), in the same order as the original list
        
        '''
        # Remove duplicates but retain list order
        unique_pmid_sent = set()
        unique_pmid_sent_list = []
        pmids_sent_text_list = list(zip(self.path_pmid_evidence,\
                                        self.path_sent_text_evidence,\
                                            self.path_evidence_link))
        for pmid_sent in pmids_sent_text_list:
            if pmid_sent not in unique_pmid_sent:
                unique_pmid_sent_list.append(pmid_sent)
                unique_pmid_sent.add(pmid_sent)
        return unique_pmid_sent_list
        
    def get_path_triples(self):
        '''
        This method returns the list of triples that make the path

        Return
        self.path_triples: list of dto.Triple
        '''
        return self.path_triples


class Node:

    '''
    This class should be used to instantiate a node object. It contains attributes of a node and used to transfer node data.
    '''
    def __init__(self,id,name) -> None:
        '''
        This is the initalization method and requires a node id and node name.
        '''
        self.id, self.name = id, name

    def get_node(self) -> tuple:
        '''
        This method returns a tuple of the node id and node name.
        '''
        return (self.id, self.name)
    
    def set_synonyms(self, alternate_names) -> None:
        '''
        This method populates the alternate names of a node, and must be used when a node has synonyms.
        '''
        self.synonyms = self.name
        if alternate_names != 'NA':
            self.synonyms = self.synonyms + ',' +alternate_names

    def get_synonyms(self):
        '''
        This method returns the alternate names of a node.
        '''
        return self.synonyms
    
    def __eq__(self, other):
        '''
        This method compares two node objects and evaluates to True if their node ids are equal
        '''
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.id == other.id
    
    def __hash__(self)  :
        '''
        This method returns the hash of the object's node id.
        '''
        return hash((self.id))
    
class Edge:

    '''
    This class should be used to instantiate an Edge object. It contains attributes of an edge and used to transfer edge data.
    '''

    def __init__(self,start_node,end_node,type):
        '''
        This is the initalization method and requires a start node, an end node and the relationship between the nodes.
        '''
        self.type = type
        self.start_node = start_node
        self.end_node = end_node

    def get_edge(self):
        '''
        This method returns a tuple of the start node, end node and the relationship b/w the nodes
        '''
        return (self.start_node, self.end_node, self.type)
    
    def get_type(self):
        '''
        This method returns the edge relationship.
        '''
        return self.type

    def set_pmid(self,pmid):
        '''
        This method must be used to set the evidence of the edge
        '''
        self.pmid = pmid
    
    def get_pmid(self):
        '''
        This method returns the edge evidence
        '''
        return self.pmid
    
    def set_sent_text(self,sent_text):
        '''
        This method is used to set the sentence text from which the relationship was originally extracted.
        '''
        self.sent_text = sent_text

    def get_sent_text(self):
        '''
        This method returns the evidence sentence text for the relationship.
        '''
        return self.sent_text
    
    def set_doc_type(self,doc_type):
        '''
        This method sets the type of evidence for the edge (book vs PMID)
        '''
        if doc_type.upper() == 'ISBN':
            self.evidence_link = CacheData.get_book_metadata(self.pmid)
        elif doc_type == 'PMID':
            self.evidence_link = 'https://pubmed.ncbi.nlm.nih.gov/'+self.pmid
        return self.evidence_link
    
    def get_evidence_link(self):
        '''
        This method returns the evidence link of the edge.
        '''
        return self.evidence_link
    
    def __eq__(self, other):
        '''
        This method compares two edge objects and evaluates to True 
        if their start nodes are same (and)
        their end nodes are same (and)
        their relationship types are same
        '''
        if not isinstance(other, type(self)):
            return NotImplemented
        return (self.start_node == other.start_node) \
            & (self.end_node == other.end_node) \
                & (self.type == other.type)

    def __hash__(self)  :
        '''
        This method returns the hash of the tuple of start node, end node and the relationship type. The three uniquely identify an edge.
        '''
        return hash((self.start_node, self.end_node, self.type))

class Triple:

    '''
    This class should be used to instantiate a Triple object. It maintains the information of a triple.
    '''

    def __init__(self,head,rel,tail):
        '''
        This is the method to initialize a Triple object. It requires a head node, a relationship and a tail node.
        
        Attributes:
        head: dto.Node
        rel: dto.Edge
        tail: dto.Node
        '''
        self.head = head
        self.rel = rel
        self.tail = tail
        self.pmid_evidence = []
        self.sent_text_evidence = []
        self.evidence_link = []

    def get_triple(self, detailed=False):
        '''
        This method returns the tuple of the head node, tail node and the relationship. 
        The head node and the tail node contains information about the node id and node name. The relationship is the edge type.
        '''
        if detailed:
            return (self.head.get_node(), \
                    self.tail.get_node(), \
                        self.rel.get_type()
                            )
        return self.head, self.rel, self.tail

    def get_evidence(self):
        '''
        This method return the evidence of the triple which includes the PMID/ISBN, sentence text and the link of the article or book.
        '''
        return self.pmid_evidence,self.sent_text_evidence,self.evidence_link
    
    def include_evidence(self, pmid, sent_text, evidence_link):
        '''
        This method sets the triple evidence.
        '''
        self.pmid_evidence.append(str(pmid))
        self.sent_text_evidence.append(sent_text)
        self.evidence_link.append(evidence_link)

    def __eq__(self, other):
        '''
        This method compares two Triple objects and evalute them as equal 
        if their head nodes are same (and)
        their tail nodes are same (and)
        their edge type is same.
        '''
        if not isinstance(other, type(self)):
            return NotImplemented
        return ((self.head == other.head) \
                & (self.tail == other.tail) \
                    & (self.rel == other.rel))

    def __hash__(self)  :
        '''
        This method returns the hash of the Triple, which is the hash object of the tuple containing the head node, tail node and relationship.
        '''
        return hash((
            self.head.get_node(),
            self.rel.get_type(),
            self.tail.get_node()
        ))