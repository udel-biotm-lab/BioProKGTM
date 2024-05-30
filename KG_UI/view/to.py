from streamlit_agraph import Node as ag_node, Edge as ag_edge

class Node:

    def __init__(self,id,label):
        self.id, self.label = id, label
    
    def set_synonyms(self,synonyms):
        self.synonyms = synonyms

    def get_node(self):
        return ag_node(id=self.id,label=self.label,size=30,font={'size':20},title=self.synonyms)
    
    def get_label(self):
        return self.label
    
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.id == other.id

    def __hash__(self)  :
        return hash((self.id))

class Edge:

    def __init__(self,source,target,label,arrow_color):
        self.label = label
        self.source = source
        self.target = target
        self.arrow_color = arrow_color

    def get_edge(self):
        return ag_edge(source=self.source,target=self.target,
                       label=self.label,
                       width=5,font={'size':12},
                       color={'color':self.arrow_color,'highlight':self.arrow_color,'hover':self.arrow_color})
    
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return (self.source == other.source) & (self.target == other.target) & (self.label == other.label)

    def __hash__(self)  :
        return hash((self.source, self.target, self.label))