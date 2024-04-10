from flax import linen as nn


class NN(nn.Module):
    """Base class for all neural network modules."""

    # All sub-modules should have the following variables:
    # params: Any = None
    # _input_transform: Optional[Callable] = None
    # _output_transform: Optional[Callable] = None

    def apply_feature_transform(self, transform):
        """Compute the features by appling a transform to the network inputs, i.e.,
        features = transform(inputs). Then, outputs = network(features).
        """

        def transform_handling_flat(x):
            """Handle inputs of shape (n,)"""
            if x.ndim == 1:
                return transform(x.reshape(1, -1)).squeeze()
            return transform(x)

        self._input_transform = transform_handling_flat

    def apply_output_transform(self, transform):
        """Apply a transform to the network outputs, i.e.,
        outputs = transform(inputs, outputs).
        """

        def transform_handling_flat(inputs, x):
            """Handle inputs of shape (n,)"""
            if x.ndim == 1:
                return transform(inputs.reshape(1, -1), x.reshape(1, -1)).squeeze()
            return transform(inputs, x)

        self._output_transform = transform_handling_flat
