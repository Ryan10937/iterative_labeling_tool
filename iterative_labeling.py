import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from utils.image_functs import *
from utils.streamlit_functs import *
import sys
import os
# sys.path.append(os.path.join(os.getcwd(),'Dataset_Generator/utils'))
from Dataset_Generator.entities import DatasetGenerator
if __name__ == '__main__':
    if len(st.session_state.keys()) == 0:
        init_session_values()
    if 'coords' not in st.session_state:
        st.session_state['coords']=[]
    
    
    st.title('Hello Streamlit')
    coords=streamlit_image_coordinates(st.session_state['current_image-label_pair'][0])
    st.session_state['coords'].append(coords)


    if 'coords' in st.session_state:
        if len(st.session_state['coords']) > 4:
            print(st.session_state['coords'])
            st.image(segment_image_with_coords(st.session_state['current_image-label_pair'][0],st.session_state['coords']))

    if st.button('Next Image'):
        st.session_state['current_image-label_pair'] = next(st.session_state['generator'])
        st.session_state['coords']=[]
   

    