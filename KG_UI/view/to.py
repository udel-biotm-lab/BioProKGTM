from streamlit_agraph import Node as ag_node, Edge as ag_edge

class Node:

    '''
    This class is a transfer object for handling node data at view.
    '''

    def __init__(self,id,label):
        '''
        Initialization requires a node id and a node label
        '''
        self.id, self.label = id, label
    
    def set_synonyms(self,synonyms):
        '''
        This method populates alternate names for a node
        '''
        self.synonyms = synonyms

    def get_node(self):
        '''
        This method creates a streamlit_agraph.Node instance with the input id and label.
        The aesthetics of the node can be updated by passing additional attributes to ag_node instantiation.
        '''
        return ag_node(id=self.id,label=self.label,size=30,font={'size':20},title=self.synonyms)
    
    def get_label(self):
        '''
        This method return the node's label.
        '''
        return self.label
    
    def __eq__(self, other):
        '''
        This method evaluates two node objects as equal if their node ids are same.
        '''
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        '''
        This method returns the hash of the node object using the node's id.
        '''
        return hash((self.id))

class Edge:

    '''
    This class is a transfer object for handling edge information at view.
    '''

    def __init__(self,source,target,label,arrow_color):
        '''
        Initialization requires a source node, target node, an edge label and an arrow color.
        The edge label and arrow color are string. The source node and target node are id's of the node.
        '''
        self.label = label
        self.source = source
        self.target = target
        self.arrow_color = arrow_color

    def get_edge(self):
        '''
        This method returns a streamlit_agraph.Edge instance for the view.to.Edge
        '''
        return ag_edge(source=self.source,target=self.target,
                       label=self.label,
                       width=5,font={'size':12},
                       color={'color':self.arrow_color,'highlight':self.arrow_color,'hover':self.arrow_color})
    
    def __eq__(self, other):
        '''
        This method evaluates two edge objects as equal if source, target and lable are same.
        '''
        if not isinstance(other, type(self)):
            return NotImplemented
        return (self.source == other.source) & (self.target == other.target) & (self.label == other.label)

    def __hash__(self)  :
        '''
        This method returns the hash value of the view.to.Edge. It creates the hash using the source node id, target node id and the edge label.
        '''
        return hash((self.source, self.target, self.label))