################################################################################
#This file is to hold functions for the user to transform a list of points into
#a label in the same form as their dataset
#The function will receive a label (class definition in Dataset_Generator repo)
################################################################################
import xmltodict
from Dataset_Generator.utils.transformation_functions import dataset_label
def coord_list_to_fashion_xml(original_label: dataset_label,label_result):
  x_list = [d['x'] for d in label_result if d != None]
  y_list = [d['y'] for d in label_result if d != None]
  
  xmin,xmax = min(x_list),max(x_list)
  ymin,ymax = min(y_list),max(y_list)

  #edit xml with label_result
  with open(original_label.label_path,'r') as f:
      label_dict=xmltodict.parse(f.read())
  if label_dict == None:
     print('label_dict is none')
     return
  label_dict['annotation']['object']['bndbox']['xmin'] = str(xmin)
  label_dict['annotation']['object']['bndbox']['ymin'] = str(ymin)
  label_dict['annotation']['object']['bndbox']['xmax'] = str(xmax)
  label_dict['annotation']['object']['bndbox']['ymax'] = str(ymax)

  xml_data = xmltodict.unparse(label_dict, pretty=True)
  # Write the XML string to a file
  with open(original_label.label_path, 'w') as file:
      file.write(xml_data)

