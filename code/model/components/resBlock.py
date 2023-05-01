import tensorflow as tf
from tensorflow.keras import layers


class SingleResBlock(layers.Layer):
    def __init__(self, params, name=None):
        #param[0] for filters, param[1] for kernel size
        super(SingleResBlock, self).__init__(name=name)
        self.conv1 = layers.Conv1D(params[0][0], params[0][1], padding='same', activation='relu')
        self.bn1 = layers.BatchNormalization()
        self.conv2 = layers.Conv1D(params[1][0], params[1][1], padding='same', activation='relu')
        self.bn2 = layers.BatchNormalization()
        self.conv3 = layers.Conv1D(params[2][0], params[2][1], padding='same')
        self.relu1 = layers.ReLU()
        self.add = layers.Add()
        self.bn3 = layers.BatchNormalization()

    def call(self, inputs):
        x = self.conv1(inputs)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.add([input, x])
        x = self.relu1(x)
        x = self.bn3(x)
        return x

