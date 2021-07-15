from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .nn import NN
from .. import activations
from .. import initializers
from .. import regularizers
from ...backend import tf


class FNN(NN):
    """Fully-connected neural network."""

    def __init__(self,
                 layer_sizes,
                 activation,
                 kernel_initializer,
                 regularization=None):
        super(FNN, self).__init__()
        self.regularizer = regularizers.get(regularization)

        self.denses = []
        activation = activations.get(activation)
        initializer = initializers.get(kernel_initializer)
        for units in layer_sizes[1:-1]:
            self.denses.append(
                tf.keras.layers.Dense(
                    units,
                    activation=activation,
                    kernel_initializer=initializer,
                    kernel_regularizer=self.regularizer
                )
            )
        self.denses.append(
            tf.keras.layers.Dense(
                layer_sizes[-1],
                kernel_initializer=initializer,
                kernel_regularizer=self.regularizer
            )
        )
        self._inputs = None
        self._targets = None
        self._data_id = None

    def call(self, inputs, training=False):
        y = inputs
        if self._input_transform is not None:
            y = self._input_transform(y)
        for f in self.denses:
            y = f(y)
        if self._output_transform is not None:
            y = self._output_transform(inputs, y) 
        return y

    @property
    def inputs(self):
        return self._inputs
    
    @inputs.setter
    def inputs(self, value):
        self._inputs = value
    
    @property
    def targets(self):
        return self._targets
    
    @targets.setter
    def targets(self, value):
        self._targets = value
    
    @property
    def data_id(self):
        return self._data_id
    
    @data_id.setter
    def data_id(self, value):
        self._data_id = value
