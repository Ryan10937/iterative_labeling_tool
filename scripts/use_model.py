
import streamlit as st

from Dataset_Generator.entities import DatasetGenerator
from Dataset_Generator.utils.transformation_functions import dataset_label 
import tensorflow as tf 
import cv2
import numpy as np
from itertools import islice
from tensorflow.keras import layers, models
import imagesize
import json
import pandas as pd
class Model():
  def __init__(self):
    self.optimizer = st.session_state['config']['optimizer']
    self.loss = st.session_state['config']['loss']
    #self.layer_config
    self.model = None
    self.generator = st.session_state['generator']
    self.batch_size = 8
    self.epochs = 5

  def compile_model(self):
    # def shallow_unet(input_shape=(None, 256, 512)):
    def shallow_unet(input_shape=(512, 512, 1)):
    # def shallow_unet(input_shape=(None, None, 3)):
      # Input layer that can take images of any size
      inputs = layers.Input(shape=input_shape)

      # Encoder path (downsampling)
      conv1 = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(inputs)
      conv1 = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(conv1)
      pool1 = layers.MaxPooling2D((2, 2))(conv1)

      conv2 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(pool1)
      conv2 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(conv2)
      pool2 = layers.MaxPooling2D((2, 2))(conv2)

      # Bottleneck
      conv3 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(pool2)
      conv3 = layers.Conv2D(128, (3, 3), activation='relu', padding='same')(conv3)

      # Decoder path (upsampling)
      up1 = layers.UpSampling2D((2, 2))(conv3)
      up1 = layers.Concatenate()([up1, conv2])
      conv4 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(up1)
      conv4 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(conv4)

      up2 = layers.UpSampling2D((2, 2))(conv4)
      up2 = layers.Concatenate()([up2, conv1])
      conv5 = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(up2)
      conv5 = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(conv5)

      # Output layer
      outputs = layers.Conv2D(1, (1, 1), activation='sigmoid')(conv5)

      # Build model
      model = models.Model(inputs, outputs)
      
      return model
    def dice_coefficient(y_true, y_pred):
      y_true = tf.cast(y_true, tf.float32)
      y_pred = tf.cast(y_pred > 0.5, tf.float32)
      intersection = tf.reduce_sum(y_true * y_pred)
      return (2 * intersection + 1) / (tf.reduce_sum(y_true) + tf.reduce_sum(y_pred) + 1)
    # Create and compile the model
    self.model = shallow_unet()
    self.model.compile(optimizer=self.optimizer, loss=self.loss, metrics=[dice_coefficient,'accuracy'])
    
    # self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

  def create_mask(self,data_label: dataset_label):
      
      """
      Creates a binary mask for a given image shape and bounding box.

      Parameters:
      - image_shape (tuple): Shape of the image, e.g., (height, width, channels).
      - bbox (dict): Dictionary containing bounding box coordinates with keys:
                    'xmin', 'xmax', 'ymin', 'ymax'.

      Returns:
      - mask (numpy array): A binary mask of the same height and width as the image.
      """
      # with open(label_path,'r') as f:
      #   bbox = json.load(f)
      bboxes = data_label.value
      # Ensure the image is at least 2D
      height, width = imagesize.get(data_label.media_path)
      
      # Create an empty mask of zeros
      mask = np.zeros((height, width), dtype=np.uint8)
      for bbox in bboxes:
        # Extract bounding box coordinates
        xmin, xmax = int(bbox['xmin']), int(bbox['xmax'])
        ymin, ymax = int(bbox['ymin']), int(bbox['ymax'])
        
        # Clip the bounding box to ensure it fits within the image dimensions
        xmin = max(0, min(xmin, width))
        xmax = max(0, min(xmax, width))
        ymin = max(0, min(ymin, height))
        ymax = max(0, min(ymax, height))

        # Draw a filled rectangle on the mask using bounding box coordinates
        try:
          mask[ymin:ymax, xmin:xmax] = 1
        except Exception as e:
          print('Error while creating mask: ',e)

      return mask

  def run_model(self):
    def batch_generator(generator, batch_size):
      while True:
        batch = list(islice(generator, batch_size))
        # If no items left to retrieve, break the loop
        if not batch:
            break
        yield batch

    def open_image(image_path):
      from PIL import Image, ImageOps
      im = ImageOps.grayscale(Image.open(image_path))
      # im = Image.open(image_path)
      return np.expand_dims(np.array(im), axis=-1) 
    
    def is_not_none(item):
      return item != None and pd.isna(item) == False
    batches = batch_generator(self.generator,self.batch_size)
    first_batch = {}
    for batch in batches:
      images = [open_image(data_label.media_path) for data_label in batch if is_not_none(data_label.media_path) and is_not_none(data_label.label_path)]
      masks = [self.create_mask(data_label) for data_label in batch if is_not_none(data_label.media_path) and is_not_none(data_label.label_path)]
      # print(images)
      # print(len(images))
      # images=np.expand_dims(images,axis=-1)
      masks=np.expand_dims(masks,axis=-1)
      if len(images) == 0 or len(masks) == 0:
        print('Empty batch')
        continue
      if len(first_batch.items())==0:
        first_batch['images'] = images
        first_batch['masks'] = masks
        continue
      
      print('Fitting model to batch of length',len(images))
      self.history = self.model.fit(x=images,y=masks,verbose=2,batch_size=len(images),epochs = 1)
      # for im,msk in zip(images,masks):
        # self.history = self.model.fit(x=[im],y=[msk],verbose=2,batch_size=len(images))
    self.evaluate_results = self.model.evaluate(first_batch['images'],first_batch['masks'])

    print(self.history)

      