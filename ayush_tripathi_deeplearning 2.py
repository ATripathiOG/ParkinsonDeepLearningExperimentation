# -*- coding: utf-8 -*-
"""Ayush Tripathi - DeepLearning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Lj7zZTfsX9iXxZyaAJcbWWFNx89BW-FS
"""

#On February 14, 2023, the data was imported from the paper of
#Little et al. (2009) from the webpage:
#https://archive.ics.uci.edu/ml/datasets/parkinsons

#import_data_modules
import pandas as pd
import requests
import io

#read_github_raw_data
url = 'https://raw.githubusercontent.com/ATripathiOG/ParkinsonDeepLearningExperimentation/main/parkinsons.csv'
download = requests.get(url).content
pksn_data = pd.read_csv(io.StringIO(download.decode('utf-8')))
print(pksn_data.shape)
print(pksn_data.columns)
pksn_data

#The following two sections (drop_name_column and split_data_into_two)
#were retrieved on February 18, 2023, from
#https://www.kaggle.com/code/ryanholbrook/stochastic-gradient-descent
#by Alexis Cook and Ryan Holbrook
#(adaptation of their code).

#drop_name_column
data = pksn_data.drop(['name'], axis=1)

#split_data_into_two
df_train = data.sample(frac=0.7, random_state=0)
df_valid = data.drop(df_train.index)

max = df_train.max(axis=0)
min = df_train.min(axis=0)
df_train = (df_train - min) / (max - min)
df_valid = (df_valid - min) / (max - min)

train_X = df_train.drop('status', axis=1)
val_X = df_valid.drop('status', axis=1)
train_y = df_train['status']
val_y = df_valid['status']

#import_deep_learning_modules
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import EarlyStopping

#early_stopping_to_prevent_overfitting
early_stopping = EarlyStopping(
    min_delta = 0.00001,
    patience=20,
    restore_best_weights = True)

#deep_learning_model
model = keras.Sequential([
    layers.Dense(units=10000, activation = 'relu', input_shape = [22]),
    layers.Dropout(rate = 0.2),
    layers.Dense(units=1000, activation = 'relu'),
    layers.Dropout(rate = 0.2),
    layers.Dense(units=100, activation = 'relu'),
    layers.Dense(units=10, activation = 'relu'),
    layers.Dense(units=1, activation = 'sigmoid')])

#optimizer_and_loss_function
model.compile(
    optimizer = 'adam',
    loss = 'binary_crossentropy',
    metrics = ['binary_accuracy'])

#fit_model_to_data
history = model.fit(
    train_X, train_y,
    validation_data = (val_X, val_y),
    batch_size = 50,
    callbacks = [early_stopping],
    epochs = 1000,
    verbose=0)

#The following two sections (validation_loss_and_accuracy and graph_val_loss_and_accuracy)
#were retrieved on February 18, 2023, 
#from https://www.kaggle.com/code/ryanholbrook/binary-classification
#by Ryan Holbrook and Alexis Cook.

#validation_loss_and_accuracy
history_df = pd.DataFrame(history.history)
history_df.loc[10:, ['loss', 'val_loss']].plot()
history_df.loc[10:, ['binary_accuracy', 'val_binary_accuracy']].plot()

#graph_val_loss_and_accuracy
print(("Best Validation Loss: {:0.4f}" +\
       "\nBest Validation Accuracy: {:0.4f}")\
      .format(history_df['val_loss'].min(),
              history_df['val_binary_accuracy'].max()))