import streamlit as st
from streamlit_agraph import Config
import pandas as pd
from PIL import Image

from view.builder import GridBuilder, GraphBuilder
from view.controller import Controller


st.set_page_config(layout='wide')

# Loads the image banner
image = Image.open('static/immerse_de.png')
st.image(image,use_column_width=True)

st.title('Bioprocess Knowledge Graph')

# Text area displaying sample queries
sample_queries = """1) What is affected by manganese?
2) What does manganese positively affect?
3) Does manganese positively affect the clinical outcome, ADCC?
4) What trace metals or minerals affect clinical outcomes and how do they affect (positive and negative correlations)?"""
st.text_area('Sample queries',sample_queries)

# Search session maintenance
if 'show_results' not in st.session_state: st.session_state.show_results = False

# Controller instantiation and retrieval of data for intial load
controller = Controller()
leaf_nodes, class_nodes, relations = controller.get_base_values()

# User input fields
st.text('Select a start node or a start node class.')
col1, col2 = st.columns(2)
st.text('Select an end node or an end node class.')
col3, col4 = st.columns(2)
col5, col6 = st.columns(2)

with col1: start_node = st.selectbox('Start Node / Subject / Affector',leaf_nodes,index=None)
with col2: start_node_class = st.selectbox('Class of Affector (subject)',class_nodes,index=None)

with col3: end_node = st.selectbox('End Node / Object / Affected',leaf_nodes,index=None)
with col4: end_node_class = st.selectbox('Class of Affected (object)',class_nodes,index=None)

with col5: relations = st.multiselect('Relationship(s)',relations)

# Values for 'Degrees of Separation' field
hop_cnt = ['1']
hop_cnt.extend(['<= '+str(i) for i in range(2,6)])
with col6:
    hop_cnt = st.selectbox('Degrees of Separation',hop_cnt)
    hop_cnt = int(hop_cnt.strip('<= '))

# Logic on click of 'Search' button
if st.button('Search', type='primary'):
    #Front end validations
    if (start_node) and (start_node_class):
        st.error("Do not select 'start node' and 'start node (class)'. Select either of the two.")
        st.session_state.show_results = False
    elif (end_node) and (end_node_class):
        st.error("Do not select 'end node' and 'end node (class)'. Select either of the two.")
        st.session_state.show_results = False
    else:
        paths = list()
        # Retrieves subclasses for user's input ontology
        start_nodes = [start_node] if start_node else controller.get_subclasses(start_node_class) if start_node_class else None
        end_nodes = [end_node] if end_node else controller.get_subclasses(end_node_class) if end_node_class else None
        # Retrieves path results matching user's input
        paths, query = controller.get_paths(start_nodes,end_nodes,relations,hop_cnt)
        # Populates user's session
        st.session_state.show_results = True
        st.session_state.paths = paths
        st.session_state.query = query


if st.session_state.show_results:
    paths = st.session_state.paths
    if len(paths) == 0:
        st.text('No results found.')
    else:
        # Builds the results section if there are results

        # Builds table view
        GridBuilder(paths).build()
        graph_container = st.container(border=True)

        # Builds graph view
        with graph_container:
            graph_builder = GraphBuilder(paths)
            graph_configurations, node_filter, graph_legend = st.columns(3)
            
            # Graph configuration components
            with graph_configurations:
                height = st.slider("height",min_value=800, max_value=1500)
                width = st.slider("width",min_value=1300, max_value=2000)
                layout = st.selectbox('layout',['repulsion','hierarchical'])
                physics = hierarchical = False
                if layout == 'hierarchical':
                    hierarchical = True
                elif layout == 'repulsion':
                    physics = True
            
            # Filter paths with the selected node(s)
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
            
            # Graph configuration based on user's selection
            config = Config(height=height, width=width, 
                            hierarchical=hierarchical, physics=physics,direction='RL',
                            improvedLayout=True,parentCentralization=False,
                    directed=True,
                    nodeHighlightBehavior=False,
                    solver='repulsion',
                    highlightColor="#F7A7A6"
                    )
            graph_builder.render(config,filter_by=selected_nodes)
        
        # Displays cypher results for user query
        if st.button('show cypher'):
            st.code("{cypher}".format(cypher=st.session_state.query))