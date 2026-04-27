__all__ = [
    # submodules
    "convert",
    "core",
    "typing",
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
    "use",
]
__version__ = "0.6.0"

# dependencies
from . import convert, core, typing
from .core import *
