import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from utils.image_functs import *
from utils.streamlit_functs import *
# from Dataset_Generator.entities import DatasetGenerator
import Dataset_Generator
if __name__ == '__main__':
    # if len(st.session_state.keys()) == 0:
    #     init_session_values()
    if 'coords' not in st.session_state:
        st.session_state['coords']=[]
    st.title('Hello Streamlit')
    coords=streamlit_image_coordinates('./dataset/bag (1).jpg')
    st.session_state['coords'].append(coords)

    if 'coords' in st.session_state:
        if len(st.session_state['coords']) > 4:
            print(st.session_state['coords'])
            st.image(segment_image_with_coords('./dataset/bag (1).jpg',st.session_state['coords']))