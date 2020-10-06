# -*- coding: utf-8 -*-
"""braille_3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Kq1NoeeD6IOJNh_W0NWsXXegQDMOs4RV
"""

import os
import tensorflow as tf

from google.colab import drive
drive.mount('/content/drive')

!ls "/content/drive/My Drive/images"

from tensorflow.keras.preprocessing.image import ImageDataGenerator

datagen = ImageDataGenerator(rescale=1/255,rotation_range=20,shear_range=10,validation_split=0.2)

train_generator = datagen.flow_from_directory('/content/drive/My Drive/images',
                                              target_size=(28,28),
                                              shuffle= True,
                                              subset='training')
validation_generator = datagen.flow_from_directory('/content/drive/My Drive/images',
                                                   target_size=(28,28),
                                                   shuffle=True,
                                                   subset='validation')

class callback(tf.keras.callbacks.Callback):
  def on_epoch_end(self,epoch,logs={}):
    ACCURACY_THRESHOLD = 0.95
    if(logs.get('val_accuracy') > ACCURACY_THRESHOLD):
      print("95% accuracy")
      self.model.stop_training = True
callbacks = callback()

model = tf.keras.models.Sequential([
                                    tf.keras.layers.Conv2D(64,(3,3),activation='relu',input_shape=(28,28,3)),
                                    tf.keras.layers.MaxPooling2D(2,2),
                                    tf.keras.layers.Conv2D(128,(3,3),activation='relu'),
                                    tf.keras.layers.MaxPooling2D(2,2),
                                    tf.keras.layers.Conv2D(256,(2,2),activation='relu'),
                                    tf.keras.layers.MaxPooling2D(2,2),
                                    tf.keras.layers.Flatten(),
                                    tf.keras.layers.Dense(256,activation='relu'),
                                    tf.keras.layers.Dense(26,activation='softmax')

])

model.summary()

model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
history = model.fit(train_generator,
                    validation_data = validation_generator,
                    epochs=150,
                    verbose=1,
                    callbacks=[callbacks]
                    )