__all__ = [
    # submodules
    "convert",
    "core",
    "typing",
    # aliases (core)
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
    # aliases (typing)
    "ArrayLike",
    "Dims",
    "Dtype",
    "Attr",
    "Attrs",
    "Coord",
    "Coords",
    "Data",
    "DataVars",
    "Factory",
    "Name",
]
__version__ = "0.7.0"

# dependencies
from . import convert, core, typing
from .core import *
from .typing import *
