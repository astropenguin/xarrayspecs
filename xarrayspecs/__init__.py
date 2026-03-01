__all__ = [
    # submodules
    "api",
    "convert",
    "spec",
    # aliases
    "AsDataArray",
    "AsDataset",
    "AsDataTree",
    "Dims",
    "Dtype",
    "Type",
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
__version__ = "0.2.0"


# dependencies
from . import api, convert, spec
from .api import *
from .spec import *
