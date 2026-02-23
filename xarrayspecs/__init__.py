__all__ = [
    # submodules
    "api",
    "spec",
    # aliases
    "Dims",
    "Dtype",
    "asdataarray",
    "asdataset",
    "asdatatree",
    "attrs",
    "dims",
    "dtype",
    "name",
    "node",
    "parse",
    "use",
]
__version__ = "0.1.0"


# dependencies
from . import api, spec
from .api import *
from .spec import *
