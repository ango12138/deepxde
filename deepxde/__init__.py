__all__ = [
    "backend",
    "callbacks",
    "data",
    "geometry",
    "grad",
    "icbc",
    "nn",
    "utils",
    "Model",
    "Variable",
]

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown version"

# Should import backend before importing anything else
from . import backend

from . import callbacks
from . import data
from . import geometry
from . import gradients as grad
from . import icbc
from . import nn
from . import utils

from .backend import Variable
from .model import Model
from .utils import saveplot

# Backward compatibility
from .icbc import (
    DirichletBC,
    NeumannBC,
    OperatorBC,
    PeriodicBC,
    RobinBC,
    PointSetBC,
    PointSetOperatorBC,
    Interface2DBC,
    IC,
)

maps = nn
