
from Dataset_Generator.entities import DatasetGenerator#need to use setuptools to add this to path
import os
import streamlit as st
from PIL import Image, ImageDraw
import numpy as np

def init_session_values():
  # import sys
  config_path = 'C:\\Users\\ryan\OneDrive\\SchoolFiles\\CSCE\Graduate\\Side_Projects\\iterative_labeling\\iterative_labeling_tool\\Dataset_Generator\\configs\\iterative_labeling.yaml'
  SCRIPT_DIR = os.path.abspath(config_path)
  st.session_state['generator'] = DatasetGenerator.Dataset_Generator(config_path).run_pipeline()
  st.session_state['current_image-label_pair'] = next(st.session_state['generator'])
  st.session_state['coords']=[]

def get_next_image():
  st.session_state['current_image-label_pair'] = next(st.session_state['generator'])
  st.session_state['loaded_image'] = Image.open(st.session_state['current_image-label_pair'][0])
  st.session_state['coords']=[]

def draw_pts_on_image():
  def get_ellipse_coords(coords):
    height=10
    width=10
    return [(coords['x']-width//2,coords['y']-height//2),(coords['x']+width//2,coords['y']+height//2)]
  draw = ImageDraw.Draw(st.session_state['loaded_image'])
  for coords in st.session_state["coords"]:
    if coords==None:
      continue
    print(get_ellipse_coords(coords))
    draw.ellipse(get_ellipse_coords(coords), fill="red")
  st.rerun()