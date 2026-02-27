__all__ = [
    # submodules
    "api",
    "new",
    "spec",
    # aliases
    "AsDataArray",
    "AsDataset",
    "AsDataTree",
    "Dims",
    "Dtype",
    "asdataarray",
    "asdataset",
    "asdatatree",
    "attrs",
    "cast",
    "dims",
    "dtype",
    "name",
    "node",
    "parse",
    "use",
]
__version__ = "0.1.0"


# dependencies
from . import api, new, spec
from .api import *
from .new import *
from .spec import *
