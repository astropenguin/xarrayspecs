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
    "Type",
    "asdataarray",
    "asdataset",
    "asdatatree",
    "attrs",
    "dims",
    "dtype",
    "name",
    "node",
    "parse",
    "type",
    "use",
]
__version__ = "0.2.0"


# dependencies
from . import api, new, spec
from .api import *
from .new import *
from .spec import *
