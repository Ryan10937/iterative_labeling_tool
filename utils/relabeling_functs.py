################################################################################
#This file is to hold functions for the user to transform a list of points into
#a label in the same form as their dataset
#The function will receive a label (class definition in Dataset_Generator repo)
################################################################################
import xmltodict
import pandas as pd
from Dataset_Generator.utils.transformation_functions import dataset_label
import streamlit as st
import os
import json
def coord_list_to_fashion_xml(original_label: dataset_label,label_result):
  

  #edit xml with label_result
  with open(original_label.label_path,'r') as f:
      label_dict=xmltodict.parse(f.read())
  if label_dict == None:
     print('label_dict is none')
     return
  if type(label_dict['annotation']['object']) == dict:
    x_list = [d['x'] for d in label_result if d != None]
    y_list = [d['y'] for d in label_result if d != None]
    
    xmin,xmax = min(x_list),max(x_list)
    ymin,ymax = min(y_list),max(y_list)

    label_dict['annotation']['object'][i]['bndbox']['xmin'] = str(xmin)
    label_dict['annotation']['object'][i]['bndbox']['ymin'] = str(ymin)
    label_dict['annotation']['object'][i]['bndbox']['xmax'] = str(xmax)
    label_dict['annotation']['object'][i]['bndbox']['ymax'] = str(ymax)
  elif type(label_dict['annotation']['object']) == list:
    for i in range(len(label_dict['annotation']['object'])):
        x_list = [d['x'] for d in label_result[i] if d != None]#label_result[i] does assume order is preserved
        y_list = [d['y'] for d in label_result[i] if d != None]
        
        xmin,xmax = min(x_list),max(x_list)
        ymin,ymax = min(y_list),max(y_list)

        label_dict['annotation']['object'][i]['bndbox']['xmin'] = str(xmin)
        label_dict['annotation']['object'][i]['bndbox']['ymin'] = str(ymin)
        label_dict['annotation']['object'][i]['bndbox']['xmax'] = str(xmax)
        label_dict['annotation']['object'][i]['bndbox']['ymax'] = str(ymax)
  xml_data = xmltodict.unparse(label_dict, pretty=True)
  # Write the XML string to a file
  with open(original_label.label_path, 'w') as file:
      file.write(xml_data)

def coord_list_to_json(original_label: dataset_label,label_result):
   
    x_list = [d['x'] for d in label_result if d != None]
    y_list = [d['y'] for d in label_result if d != None]
  
    xmin,xmax = min(x_list),max(x_list)
    ymin,ymax = min(y_list),max(y_list)
    if original_label.label_path == None or pd.isna(original_label.label_path):
        label_dict = {}
        original_label.label_path = st.session_state['data_generator_config']['label_folder']
    else:
        with open(original_label.label_path,'r') as f:
            label_dict=json.load(f)
    if label_dict == None:
        print('label_dict is none')
        return
    label_dict['xmin'] = xmin
    label_dict['xmax'] = xmax
    label_dict['ymin'] = ymin
    label_dict['ymax'] = ymax
    label_dict['image_path'] = original_label.media_path
    label_name = original_label.media_path.split('\\')[-1].split('.')[0] + '.json'
    try:
        with open(os.path.join(original_label.label_path,label_name), 'w') as f:
            json.dump(label_dict,f)
        st.success('Successfully saved label to file'+os.path.join(original_label.label_path,label_name))
    except:
        st.error('Could not save label to file'+os.path.join(original_label.label_path,label_name))