import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from utils.image_functs import *
from utils.streamlit_functs import *
from utils.relabeling_functs import *
import sys
import os
from Dataset_Generator.entities import DatasetGenerator

if __name__ == '__main__':
    st.title('Iterative Labeling')
    #####################################################################
    #################### Initialize values ##############################
    if len(st.session_state.keys()) == 0:
        init_session_values()
        get_next_image()
    
    #####################################################################
    
    #####################################################################
    ########################### Buttons #################################
    with st.sidebar:
        index = st.number_input('Current Index: ',step=1,value=st.session_state['image_num'])
        st.text('Out of '+str(st.session_state['total_indecies']))
        if st.button('Next Image'):
            if index==st.session_state['image_num']:
                get_next_image()
            else:
                jumps=index-st.session_state['image_num']
                # jumps=index
                if jumps < 0:
                    jumps=0
                    st.error('Cannot jump to previous indecies, refresh page to start at 0')
                for _ in range(jumps):
                    get_next_image()
        if st.button('Submit label'):
            save_label(st.session_state['current_image-label_pair'],st.session_state['coords'])

        if st.button('Clear'):
            st.session_state['coords']=[[]]
            st.session_state['loaded_image']=Image.open(st.session_state['current_image-label_pair'].media_path)
            draw_existing_label_on_image()
        if st.button('Train Model'):
            train_model()
        
        # config_path = st.text_input('Config Path', value="")
        # if config_path != None:
        #     st.session_state['config_path'] = config_path
        #     with open('cache/configpath.txt','r') as f:
        #         st.session_state['config_path'] = f.read()
        # else: 
        #     with open('cache/configpath.txt','r') as f:
        #         st.session_state['config_path'] = f.read()
    #####################################################################
    

    #####################################################################
    ######################### Label Coords ##############################
    coords=streamlit_image_coordinates(st.session_state['loaded_image'])
    if st.session_state['current_image-label_pair'].value != None and st.session_state['has_drawn_existing']==False:
        draw_existing_label_on_image()
    if coords != None and coords not in st.session_state['coords']:
        if len(st.session_state['coords']) % 4 == 0:
            st.session_state['coords'].append([])

        st.session_state['coords'][-1].append(coords)
        draw_pts_on_image()

    if 'coords' in st.session_state:
        print("st.session_state['coords']",st.session_state['coords'])
        if len(st.session_state['coords'][-1]) >= 4:
            st.image(segment_image_with_coords(st.session_state['current_image-label_pair'].media_path,st.session_state['coords']))
    if st.session_state['current_image-label_pair'].value != None:
        st.text(st.session_state['current_image-label_pair'].value)
    #####################################################################

    

    