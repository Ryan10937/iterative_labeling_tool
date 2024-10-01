
from Dataset_Generator.entities import DatasetGenerator#need to use setuptools to add this to path
import os
import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import yaml
import utils.relabeling_functs as rfuncts
import inspect
def init_session_values():
  # import sys
  def open_config(config_path):
    with open(config_path) as f:
      try:
          config = yaml.safe_load(f)
      except yaml.YAMLError as exc:
          print(exc)
          return None
    return config
  st.session_state['config'] = open_config('configs/fashion_segmentation.yaml')#this path will need to be args
  dataset_config_path = st.session_state['config']['dataset_generator_config_path']
  st.session_state['generator'] = DatasetGenerator.Dataset_Generator(dataset_config_path).run_pipeline()
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
  if label == None:
    return
  else:
    print('label in draw_existing',label)
  for coords in [{'x':label['xmin'],'y':label['ymin']},
                 {'x':label['xmin'],'y':label['ymax']},
                 {'x':label['xmax'],'y':label['ymin']},
                 {'x':label['xmax'],'y':label['ymax']},
                 ]:
    draw.ellipse(get_ellipse_coords(coords), fill="blue")
  st.session_state['has_drawn_existing']=True
  st.rerun()
  

def save_label(image_label_pair,new_label):
   functions = inspect.getmembers(rfuncts,inspect.isfunction)
   save_label_function = [y for x,y in functions if x==st.session_state['config']['label_saving_function']][0]
   save_label_function(image_label_pair,new_label)