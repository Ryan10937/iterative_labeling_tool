
from Dataset_Generator.entities import DatasetGenerator#need to use setuptools to add this to path
import os

def init_session_values():
  import streamlit as st
  # import sys
  config_path = 'C:\\Users\\ryan\OneDrive\\SchoolFiles\\CSCE\Graduate\\Side_Projects\\iterative_labeling\\iterative_labeling_tool\\Dataset_Generator\\configs\\iterative_labeling.yaml'
  SCRIPT_DIR = os.path.abspath(config_path)
  # sys.path.append(os.path.dirname(SCRIPT_DIR))
  st.session_state['generator'] = DatasetGenerator.Dataset_Generator(config_path).run_pipeline()
  st.session_state['current_image-label_pair'] = next(st.session_state['generator'])