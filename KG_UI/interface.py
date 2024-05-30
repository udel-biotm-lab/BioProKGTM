import streamlit as st
from streamlit_agraph import Config
import pandas as pd
from PIL import Image
from service.relation_service import RelationService
from service.dictionary_service import DictionaryService
from service.ontology_service import OntologyService

from view.builder import GridBuilder, GraphBuilder

st.set_page_config(layout='wide')

image = Image.open('/home/manjua/workspace/waters_kg/immerse_de.png')
st.image(image,use_column_width=True)

st.title('Bioprocess Knowledge Graph')

sample_queries = """1) What is affected by manganese?
2) What does manganese positively affect?
3) Does manganese positively affect the clinical outcome, ADCC?
4) What trace metals or minerals affect clinical outcomes and how do they affect (positive and negative correlations)?"""
st.text_area('Sample queries',sample_queries)

if 'show_results' not in st.session_state: st.session_state.show_results = False

st.text('Select a start node or a start node class.')
col1, col2 = st.columns(2)
st.text('Select an end node or an end node class.')
col3, col4 = st.columns(2)
col5, col6 = st.columns(2)

dictionary_service = DictionaryService()
ontology_service = OntologyService()
relation_service = RelationService()

@st.cache_data
def retrieve_base_values():
    leaf_nodes = dictionary_service.get_canonical_names()
    class_nodes = ontology_service.get_ontology_names()
    relations = relation_service.get_possible_relationships()
    return leaf_nodes, class_nodes, relations

leaf_nodes, class_nodes, relations = retrieve_base_values()
with col1: start_node = st.selectbox('Start Node / Subject / Affector',leaf_nodes,index=None)
with col2: start_node_class = st.selectbox('Class of Affector (subject)',class_nodes,index=None)

with col3: end_node = st.selectbox('End Node / Object / Affected',leaf_nodes,index=None)
with col4: end_node_class = st.selectbox('Class of Affected (object)',class_nodes,index=None)

with col5: relations = st.multiselect('Relationship(s)',relations)

hop_cnt = ['1']
hop_cnt.extend(['<= '+str(i) for i in range(2,6)])
with col6:
    hop_cnt = st.selectbox('Degrees of Separation',hop_cnt)
    hop_cnt = int(hop_cnt.strip('<= '))

if st.button('Search', type='primary'):
    if (start_node) and (start_node_class):
        st.error("Do not select 'start node' and 'start node (class)'. Select either of the two.")
        st.session_state.show_results = False
    elif (end_node) and (end_node_class):
        st.error("Do not select 'end node' and 'end node (class)'. Select either of the two.")
        st.session_state.show_results = False
    else:
        paths = list()
        start_nodes = [start_node] if start_node else ontology_service.get_dictionary_canonical_names(start_node_class) if start_node_class else None
        end_nodes = [end_node] if end_node else ontology_service.get_dictionary_canonical_names(end_node_class) if end_node_class else None
        paths, query = relation_service.get_ontological_impact_relations(start_nodes,end_nodes,relations,hop_cnt)
        st.session_state.show_results = True
        st.session_state.paths = paths
        st.session_state.query = query


if st.session_state.show_results:
    paths = st.session_state.paths
    if len(paths) == 0:
        st.text('No results found.')
    else:
        GridBuilder(paths).build()
        graph_container = st.container(border=True)
        with graph_container:
            graph_builder = GraphBuilder(paths)
            graph_configurations, node_filter, graph_legend = st.columns(3)
            with graph_configurations:
                height = st.slider("height",min_value=800, max_value=1500)
                width = st.slider("width",min_value=1300, max_value=2000)
                layout = st.selectbox('layout',['repulsion','hierarchical'])
                physics = hierarchical = False
                if layout == 'hierarchical':
                    hierarchical = True
                elif layout == 'repulsion':
                    physics = True
            with node_filter:
                selected_nodes = st.multiselect('Affector/Affected',graph_builder.get_node_labels())
            with graph_legend:
                st.write("")
                legend_data = pd.DataFrame(list(GraphBuilder.edge_label_abbr.items()),columns=['Edge','Label'])
                st.data_editor(
                        legend_data,
                        hide_index=True,
                        disabled=True
                    )
            
            config = Config(height=height, width=width, 
                            hierarchical=hierarchical, physics=physics,direction='RL',
                            improvedLayout=True,parentCentralization=False,
                    directed=True,
                    nodeHighlightBehavior=False,
                    solver='repulsion',
                    highlightColor="#F7A7A6"
                    )
            graph_builder.render(config,filter_by=selected_nodes)
        if st.button('show cypher'):
            st.code("{cypher}".format(cypher=st.session_state.query))