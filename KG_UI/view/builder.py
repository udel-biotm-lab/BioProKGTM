from view.to import Node, Edge
from streamlit_agraph import agraph
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import matplotlib.colors as mcolors
import pandas as pd

class GraphBuilder:

    '''
    This class is responsible for handling tasks related to building the graph results view
    '''

    # Edge color mapping for the current impact relationships
    edge_colors = {'POSITIVELY_CORRELATED':mcolors.to_hex('green'),\
                   'NEGATIVELY_CORRELATED':mcolors.to_hex('red'), \
                    'NOT_CORRELATED':mcolors.to_hex('orange'),\
                        'CORRELATED_NOT_SPECIFIED':mcolors.to_hex('blue')}
    
    # Edge abbreviation mapping for the current impact relationships
    edge_label_abbr = {'POSITIVELY_CORRELATED':'POS_CORR',\
                   'NEGATIVELY_CORRELATED':'NEG_CORR', \
                    'NOT_CORRELATED':'NT_CORR',\
                        'CORRELATED_NOT_SPECIFIED':'CORR_NT_SPEC'}

    def __init__(self, impact_paths):
        '''
        Initializing the graph builder requires the list of paths
        '''
        self.impact_paths = impact_paths
        self.nodes, self.edges = self._build(self.impact_paths)
    
    def _build(self,paths):
        '''
        This method builds the graph components from the input paths
        '''
        nodes = set()
        edges = set()
        for impact_path in paths:
            for triple in impact_path.get_path_triples():
                head, rel, tail = triple.get_triple()
                head_id, head_label = head.get_node(); tail_id, tail_label = tail.get_node()
                edge_color = GraphBuilder.edge_colors.get(rel.get_type())
                if edge_color:
                    head_node = Node(head_id, head_label)
                    head_node.set_synonyms(head.get_synonyms())
                    nodes.add(head_node)
                    tail_node = Node(tail_id, tail_label)
                    tail_node.set_synonyms(tail.get_synonyms())
                    nodes.add(tail_node)
                    edges.add(Edge(head_id,tail_id,GraphBuilder.edge_label_abbr.get(rel.get_type()),edge_color))
                else: print('Invalid edge relation type for display:',rel.get_type())
        return nodes, edges

    def render(self, config, filter_by=None):
        '''
        This method renders the graph based on the input user configurations.
        '''
        selected_paths = set()
        if filter_by:
            for select_node in filter_by:
                for impact_path in self.impact_paths:
                    path_nodes = impact_path.get_path_nodes()
                    if select_node in path_nodes:
                        selected_paths.add(impact_path)
        else:
            selected_paths =self.impact_paths
        nodes, edges = self._build(selected_paths)
        edges = [edge.get_edge() for edge in edges]
        nodes = [node.get_node() for node in nodes]
        graph_component = agraph(nodes, edges, config)
        return graph_component
    
    def get_node_labels(self):
        '''
        This method returns the unique list of node labels in the graph
        '''
        node_labels = set()
        for node in self.nodes:
            node_labels.add(node.get_label())
        return sorted(list(node_labels))
      

class GridBuilder:

    '''
    This class is responsible for handling tasks related to building the table view of the results.
    '''

    def __init__(self, paths):
        '''
        Initializing the grid builder requires the list of paths.
        '''
        self.paths = paths
    
    def build(self):
        '''
        This method builds the table with the results using the path data. It creates hyperlink for the evidence.
        '''
        output = list()
        for result in self.paths:
            path, evidence = result.get_final_route(), result.get_path_evidence()
            pmid_sent_link = "^PMID_sep^".join(str(x[0])+'<|>'+x[1]+'<|>'+x[2] for x in evidence)
            output.append((path, pmid_sent_link))
        data = pd.DataFrame(output, columns=['Path','PMID/ISBN'])
        
        gb = GridOptionsBuilder.from_dataframe(data)
        gb.configure_column(
        "PMID/ISBN", "PMID/ISBN",
        cellRenderer=JsCode("""
            class UrlCellRenderer {
            init(params) {            
                this.eGui = document.createElement('div');
                this.eGui.innerHTML = '';
                var param_pmids = params.value.split('^PMID_sep^');
                for (var i=0; i<param_pmids.length; i++){
                    var pmid_sent_link = param_pmids[i].split('<|>');
                    var pmid = pmid_sent_link[0];
                    var sentence = pmid_sent_link[1];
                    var evidence_URL = pmid_sent_link[2];                    
                    var href_content = "<a href='"+evidence_URL+"'><span title='"+sentence+"'>"+pmid+"</span></a>";
                    if ((param_pmids.length - i) > 1) {
                        href_content = href_content+',';
                    }
                    this.eGui.innerHTML = this.eGui.innerHTML+href_content;
                }
                var hrefs = this.eGui.getElementsByTagName('a');
                for (var i=0; i<hrefs.length; i++){
                    hrefs[i].setAttribute('target', '_blank');
                }                        
            }
            getGui() {
                return this.eGui;
            }
            }
        """)
        )
        gb.configure_pagination(enabled=True, paginationAutoPageSize=False, paginationPageSize=10)

        AgGrid(
            data, 
            gridOptions=gb.build(), 
            autoHeight=True,
            width='100%',
            allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
            enable_enterprise_modules=False, 
            fit_columns_on_grid_load=True,
            reload_data=False
            )