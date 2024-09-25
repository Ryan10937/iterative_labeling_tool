import numpy as np
from PIL import Image
def segment_image_with_coords(image_path,coord_list):
  image = open_image(image_path)
  x_list = [d['x'] for d in coord_list if d != None]
  y_list = [d['y'] for d in coord_list if d != None]
  
  xmin,xmax = min(x_list),max(x_list)
  ymin,ymax = min(y_list),max(y_list)

  print(xmin,xmax,ymin,ymax)
  return image[ymin:ymax,xmin:xmax]
def open_image(image_path):
  return np.array(Image.open(image_path))