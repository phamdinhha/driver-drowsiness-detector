from keras.layers import Dense, Flatten, Dropout, ZeroPadding3D
from keras.layers.recurrent import LSTM
from keras.models import Sequential, load_model
from keras.optimizers import Adam, RMSprop
from keras.layers.wrappers import TimeDistributed
from keras.layers.convolutional import (Conv2D, MaxPooling3D, Conv3D,MaxPooling2D)
from collections import deque
import sys

class ResearchModels():
    def __init__(self, nb_classes, seq_length, input_shape,
                 saved_model=None, features_length=2048):

        # Set defaults.
        self.seq_length = seq_length
        self.load_model = load_model
        self.saved_model = saved_model
        self.nb_classes = nb_classes
        self.feature_queue = deque()
        self.input_shape = input_shape

    def lstm(self):
        """Build a simple LSTM network. We pass the extracted features from
        our CNN to this model predomenently."""
        # Model.
	    #print(self.input_shape)
        model = Sequential()
        model.add(LSTM(2048, return_sequences=True, input_shape=self.input_shape,dropout=0.5))
        model.add(Flatten())
        model.add(Dense(1024, activation='relu'))
        model.add(Dense(512, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.nb_classes, activation='softmax'))
        return model

    def trainingModel(self, input_shape):
        metrics = ['accuracy']
        self.input_shape = input_shape
        self.model = self.lstm()
        # Now compile the network.
        optimizer = Adam(lr=0.00005)
        self.model.compile(loss='categorical_crossentropy', optimizer=optimizer,
                           metrics=metrics)
        print(self.model.summary())
    
    def loadModelFromPath(self, weight_path):
        model = self.lstm()
        model.load_weights(weight_path)
        return model

    
