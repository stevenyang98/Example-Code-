# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 16:11:47 2018

@author: Michael Carolan, Steven Yang
"""
import IAP
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


def train(ticker1, ticker2, value, date_range, n_ep, show=False):
    """
    Train over the length dataset over n_ep epochs, contructing a graph of loss
    over time if show.
    
    n_ep: integer representing the number of epochs to train over
    
    show: boolean indicating whether to graph loss and accuracy or not
    """
    
    #Load proper data
    stock1 = IAP.get_data(ticker1, value, date_range)
    stock2 = IAP.get_data(ticker2, value, date_range)
    
    #Set aside 1/3 for test data
    train_s1, val_s1, train_s2, val_s2 = train_test_split(stock1, stock2, test_size=.1, random_state=42)
            
    # Build network, 2 hidden layers, 26 dimensional vectors for alphabet
    model = keras.Sequential()
    model.add(keras.layers.Embedding(2, 16)) #26=numletters
    model.add(keras.layers.GlobalAveragePooling1D())
    model.add(keras.layers.Dense(16, activation=tf.nn.relu))
    model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))
    
    # Loss function, Using Probabilities
    model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='binary_crossentropy',
              metrics=['accuracy'])
    
    # Perform n_ep epochs of training on train_data
    test_s1 = IAP.get_data(ticker1, value, (date_range[1], 2020))
    test_s2 = IAP.get_data(ticker2, value, (date_range[1], 2020))
    
    history = model.fit(train_s1,
                        train_s2,
                        epochs=n_ep,
                        batch_size=64,
                        validation_data=(val_s1, val_s2), 
                        shuffle=True,
                        verbose=1)
    
    #EVALUATE THE FINAL MODEL

    results = model.evaluate(test_s1, test_s2)
    print(results)
    
    # GRAPH ACCURACY AND LOSS OVER TIME
    if show:
        acc = history.history['acc']
        val_acc = history.history['val_acc']
        loss = history.history['loss']
        val_loss = history.history['val_loss']
        
        history_dict = history.history
        
        epochs = range(1, len(acc) + 1)
        
        # "bo" is for "blue dot"
        plt.plot(epochs, loss, 'bo', label='Training loss')
        # b is for "solid blue line"
        plt.plot(epochs, val_loss, 'b', label='Validation loss')
        plt.title('Training and validation loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        
        plt.show()
        
        plt.clf()   # clear figure
        acc_values = history_dict['acc']
        val_acc_values = history_dict['val_acc']
        
        plt.plot(epochs, acc, 'bo', label='Training acc')
        plt.plot(epochs, val_acc, 'b', label='Validation acc')
        plt.title('Training and validation accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()
        
        plt.show()
        
    return model
    