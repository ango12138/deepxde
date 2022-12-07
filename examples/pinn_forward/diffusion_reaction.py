"""Backend supported: tensorflow.compat.v1, tensorflow, pytorch"""
import deepxde as dde
import numpy as np
import deepxde.backend as bkd


def pde(x, y):
    dy_t = dde.grad.jacobian(y, x, i=0, j=1)
    dy_xx = dde.grad.hessian(y, x, i=0, j=0)
    d = 1
    return (
        dy_t
        - d * dy_xx
        - bkd.exp(-x[:, 1:])
        * (
            3 * bkd.sin(2 * x[:, 0:1]) / 2
            + 8 * bkd.sin(3 * x[:, 0:1]) / 3
            + 15 * bkd.sin(4 * x[:, 0:1]) / 4
            + 63 * bkd.sin(8 * x[:, 0:1]) / 8
        )
    )

def func(x):
    return np.exp(-x[:, 1:]) * (
        np.sin(x[:, 0:1])
        + np.sin(2 * x[:, 0:1]) / 2
        + np.sin(3 * x[:, 0:1]) / 3
        + np.sin(4 * x[:, 0:1]) / 4
        + np.sin(8 * x[:, 0:1]) / 8
    )


geom = dde.geometry.Interval(-np.pi, np.pi)
timedomain = dde.geometry.TimeDomain(0, 1)
geomtime = dde.geometry.GeometryXTime(geom, timedomain)

data = dde.data.TimePDE(
    geomtime, pde, [], num_domain=320, solution=func, num_test=80000
)

layer_size = [2] + [30] * 6 + [1]
activation = "tanh"
initializer = "Glorot uniform"
net = dde.nn.FNN(layer_size, activation, initializer)

def output_transform(x, y):
    return (
        x[:, 1:2] * (np.pi ** 2 - x[:, 0:1] ** 2) * y
        + bkd.sin(x[:, 0:1])
        + bkd.sin(2 * x[:, 0:1]) / 2
        + bkd.sin(3 * x[:, 0:1]) / 3
        + bkd.sin(4 * x[:, 0:1]) / 4
        + bkd.sin(8 * x[:, 0:1]) / 8
    )

net.apply_output_transform(output_transform)

model = dde.Model(data, net)
model.compile("adam", lr=1e-3, metrics=["l2 relative error"])
losshistory, train_state = model.train(iterations=20000)

dde.saveplot(losshistory, train_state, issave=True, isplot=True)
