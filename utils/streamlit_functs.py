
from Dataset_Generator.entities import DatasetGenerator,ConfigReader#need to use setuptools to add this to path
import os
import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import yaml
import utils.relabeling_functs as rfuncts
import inspect
from scripts.use_model import Model
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
  def get_config_path_from_cache(cache_path):
    with open(cache_path,'r') as f:
      path = f.read()
    return path
  st.session_state['config'] = open_config('configs/fashion_segmentation.yaml')#this path will need to be args
  # st.session_state['config'] = open_config(get_config_path_from_cache('cache/configpath.txt'))#this path will need to be args
  dataset_config_path = st.session_state['config']['dataset_generator_config_path']
  st.session_state['data_generator_config'] = ConfigReader.Config_Reader(dataset_config_path).open_config()
  st.session_state['Dataset_Generator'] = DatasetGenerator.Dataset_Generator(dataset_config_path)
  st.session_state['generator'] = st.session_state['Dataset_Generator'].run_pipeline()
  st.session_state['current_image-label_pair'] = next(st.session_state['generator'])
  st.session_state['coords']=[[]]
  st.session_state['image_num']=0
  st.session_state['total_indecies'] = len(st.session_state['Dataset_Generator'].dataset_labels)

def get_next_image():
  st.session_state['current_image-label_pair'] = next(st.session_state['generator'])
  st.session_state['loaded_image'] = Image.open(st.session_state['current_image-label_pair'].media_path)
  st.session_state['coords']=[[]]
  st.session_state['has_drawn_existing']=False
  st.session_state['image_num'] += 1
  # print('here in get_next_image')

def draw_pts_on_image():
  def get_ellipse_coords(coords):
    height=10
    width=10
    return [(coords['x']-width//2,coords['y']-height//2),(coords['x']+width//2,coords['y']+height//2)]
  draw = ImageDraw.Draw(st.session_state['loaded_image'])

  for coord_group in st.session_state["coords"]:
    for coords in coord_group:
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
  label_arr = st.session_state['current_image-label_pair'].value
  if label_arr == None:
    return
  for label in label_arr:
    if label == None:
      return
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


def train_model():
  st.session_state['model'] = Model()
  st.session_state['model'].compile_model()
  st.session_state['model'].run_model()
