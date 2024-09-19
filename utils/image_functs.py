def segment_image_with_coords(image_path,coord_list):
  image = open_image(image_path)
  x_list = [d['x'] for d in coord_list if d != None]
  y_list = [d['y'] for d in coord_list if d != None]
  
  xmin,xmax = min(x_list),max(x_list)
  ymin,ymax = min(y_list),max(y_list)

  return image[xmin:xmax,ymin:ymax]
def open_image(image_path):
  from PIL import Image
  import numpy as np
  return np.array(Image.open(image_path))