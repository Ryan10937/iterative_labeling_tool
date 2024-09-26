
from Dataset_Generator.entities import DatasetGenerator#need to use setuptools to add this to path
import os
import streamlit as st
from PIL import Image, ImageDraw
import numpy as np

def init_session_values():
  # import sys
  config_path = 'C:\\Users\\ryan\OneDrive\\SchoolFiles\\CSCE\Graduate\\Side_Projects\\iterative_labeling\\iterative_labeling_tool\\Dataset_Generator\\configs\\iterative_labeling.yaml'
  st.session_state['generator'] = DatasetGenerator.Dataset_Generator(config_path).run_pipeline()
  st.session_state['current_image-label_pair'] = next(st.session_state['generator'])
  st.session_state['coords']=[]

def get_next_image():
  st.session_state['current_image-label_pair'] = next(st.session_state['generator'])
  st.session_state['loaded_image'] = Image.open(st.session_state['current_image-label_pair'].media_path)
  st.session_state['coords']=[]
  st.session_state['has_drawn_existing']=False
  # print('here in get_next_image')

def draw_pts_on_image():
  def get_ellipse_coords(coords):
    height=10
    width=10
    return [(coords['x']-width//2,coords['y']-height//2),(coords['x']+width//2,coords['y']+height//2)]
  draw = ImageDraw.Draw(st.session_state['loaded_image'])

  for coords in st.session_state["coords"]:
    if coords==None:
      continue
    draw.ellipse(get_ellipse_coords(coords), fill="red")
  st.rerun()


def draw_existing_label_on_image():
  def get_ellipse_coords(coords):
    height=10
    width=10
    return [(coords['x']-width//2,coords['y']-height//2),(coords['x']+width//2,coords['y']+height//2)]
  draw = ImageDraw.Draw(st.session_state['loaded_image'])
  label = st.session_state['current_image-label_pair'].value
  for coords in [{'x':label['xmin'],'y':label['ymin']},
                 {'x':label['xmin'],'y':label['ymax']},
                 {'x':label['xmax'],'y':label['ymin']},
                 {'x':label['xmax'],'y':label['ymax']},
                 ]:
    draw.ellipse(get_ellipse_coords(coords), fill="blue")
  st.session_state['has_drawn_existing']=True
  st.rerun()
  