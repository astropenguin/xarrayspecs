__all__ = [
    # submodules
    "api",
    "convert",
    # aliases
    "AsDataArray",
    "AsDataset",
    "AsDataTree",
    "asdataarray",
    "asdataset",
    "asdatatree",
    "attrs",
    "dims",
    "dtype",
    "name",
    "node",
    "type",
    "use",
]
__version__ = "0.6.0"

# dependencies
from . import api, convert
from .api import *
