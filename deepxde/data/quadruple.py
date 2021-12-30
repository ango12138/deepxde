from .data import Data
from .sampler import BatchSampler


class QuadrupleCartesianProd(Data):
    """Cartesian Product input data format for BioNet architecture.

    This dataset can be used with the network ``BiONetCartesianProd`` for operator
    learning.

    Args:
        X_train: A tuple of three NumPy arrays. The first element has the shape (`N1`,
            `dim1`), the second element has the shape (`N1`, `dim2`), and the third
            element has the shape (`N2`, `dim3`).
        y_train: A NumPy array of shape (`N1`, `N2`).
    """

    def __init__(self, X_train, y_train, X_test, y_test):
        if (
            len(X_train[0]) * len(X_train[2]) != y_train.size
            or len(X_train[1]) * len(X_train[2]) != y_train.size
            or len(X_train[0]) != len(X_train[1])
        ):
            raise ValueError(
                "The training dataset does not have the format of Cartesian product."
            )
        if (
            len(X_test[0]) * len(X_test[2]) != y_test.size
            or len(X_test[1]) * len(X_test[2]) != y_test.size
            or len(X_test[0]) != len(X_test[1])
        ):
            raise ValueError(
                "The testing dataset does not have the format of Cartesian product."
            )
        self.train_x, self.train_y = X_train, y_train
        self.test_x, self.test_y = X_test, y_test

        self.train_sampler = BatchSampler(len(X_train[0]), shuffle=True)

    def losses(self, targets, outputs, loss, model):
        return [loss(targets, outputs)]

    def train_next_batch(self, batch_size=None):
        if batch_size is None:
            return self.train_x, self.train_y
        indices = self.train_sampler.get_next(batch_size)
        return (
            self.train_x[0][indices],
            self.train_x[1][indices],
            self.train_x[2],
        ), self.train_y[indices]

    def test(self):
        return self.test_x, self.test_y
