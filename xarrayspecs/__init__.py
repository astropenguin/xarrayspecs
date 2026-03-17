__all__ = [
    # submodules
    "convert",
    "core",
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
__version__ = "0.6.0"

# dependencies
from . import convert, core, spec
from .core import *
from .spec import *
