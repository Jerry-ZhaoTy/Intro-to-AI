"""
Created on Nov 22 2020

@author: Tianyi Zhao
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np


def get_dataset(training=True):
    mnist = keras.datasets.mnist
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()
    if training:
        return (train_images, train_labels)
    return (test_images, test_labels)

def print_stats(train_images, train_labels):  
    class_names = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    print(len(train_images))
    shape = train_images[0].shape
    print(shape[0], 'x', shape[1], sep='')
    labels = [0,0,0,0,0,0,0,0,0,0]
    for j in range(0,len(labels)):
        for i in range (0,len(train_labels)):
            if j == train_labels[i]:
                labels[j] = labels[j]+1
    print('0.', class_names[0], '-', int(labels[0]))
    print('1.', class_names[1], '-', int(labels[1]))
    print('2.', class_names[2], '-', int(labels[2]))
    print('3.', class_names[3], '-', int(labels[3]))
    print('4.', class_names[4], '-', int(labels[4]))
    print('5.', class_names[5], '-', int(labels[5]))
    print('6.', class_names[6], '-', int(labels[6]))
    print('7.', class_names[7], '-', int(labels[7]))
    print('8.', class_names[8], '-', int(labels[8]))
    print('9.', class_names[9], '-', int(labels[9]))

def build_model():
    model = keras.Sequential(
        [
            layers.Flatten(input_shape=(28,28)),
            layers.Dense(128, activation="relu"),
            layers.Dense(64, activation="relu"),
            layers.Dense(10),
        ]
    )
    
    model.compile(
        optimizer=keras.optimizers.SGD(
            learning_rate=0.001, momentum=0.0, nesterov=False, name="SGD",),
        loss=keras.losses.SparseCategoricalCrossentropy(
            from_logits=True, reduction="auto", name="sparse_categorical_crossentropy"),
        metrics=['accuracy'],
    )
    
    return model


def train_model(model, train_images, train_labels, T): 
    model.fit(    
        x=train_images,
        y=train_labels,
        epochs=T,
    )
    
def evaluate_model(model, test_images, test_labels, show_loss=True):
    test_loss, test_accuracy = model.evaluate(test_images, test_labels,verbose=0,)
    
    test_loss = "{:.4f}".format(test_loss)
    test_accuracy = "{0:.2%}".format(test_accuracy)
    
    if show_loss:
        print ("Loss:",test_loss)
    print("Accuracy:",test_accuracy)
    
    
def predict_label(model, test_images, index):
    class_names = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
    
    result = model.predict(test_images)
    
    index_result = result[index]
    first = -1
    first_label = ''
    second = -1
    second_label = ''
    third = -1
    third_label = ''
    for i in range(0, len(index_result)): 
        if (index_result[i] > first): 
            third = second 
            second = first 
            third_label = second_label
            second_label = first_label
            first = index_result[i] 
            first_label = class_names[i]
        elif (index_result[i] > second): 
            third = second 
            second = index_result[i] 
            third_label = second_label
            second_label = class_names[i]
        elif (index_result[i] > third): 
            third = index_result[i] 
            third_label = class_names[i]
        
    print(first_label,": ","{0:.2%}".format(first),sep='')
    print(second_label,": ","{0:.2%}".format(second),sep='')
    print(third_label,": ","{0:.2%}".format(third),sep='')

(train_images, train_labels) = get_dataset()
(test_images, test_labels) = get_dataset(False)
model = build_model()
train_model(model, train_images, train_labels, 1)
evaluate_model(model, test_images, test_labels)
model.add(layers.Softmax())#for predict
predict_label(model, test_images, 1)





