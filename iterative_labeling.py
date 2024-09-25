import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from utils.image_functs import *
from utils.streamlit_functs import *
from utils.relabeling_functs import *
import sys
import os
# sys.path.append(os.path.join(os.getcwd(),'Dataset_Generator/utils'))
from Dataset_Generator.entities import DatasetGenerator
if __name__ == '__main__':
    if len(st.session_state.keys()) == 0:
        init_session_values()
        get_next_image()
    
    
    st.title('Hello Streamlit')

    if st.button('Clear'):
        st.session_state['coords']=[]
        st.session_state['loaded_image']=Image.open(st.session_state['current_image-label_pair'].media_path)
    
    if st.button('Next Image'):
        get_next_image()
    coords=streamlit_image_coordinates(st.session_state['loaded_image'])
    # print('coords:',coords)
    if coords != None and coords not in st.session_state['coords']:
        st.session_state['coords'].append(coords)
        draw_pts_on_image()
    # print(st.session_state["coords"])

    if 'coords' in st.session_state:
        if len(st.session_state['coords']) >= 4:
            #show coords sub-image
            print(st.session_state['coords'])
            st.image(segment_image_with_coords(st.session_state['current_image-label_pair'].media_path,st.session_state['coords']))
    if st.session_state['current_image-label_pair'].value != None:
        st.text(st.session_state['current_image-label_pair'].value)

    if st.button('edit_label'):
        coord_list_to_fashion_xml(st.session_state['current_image-label_pair'],st.session_state['coords'])

    