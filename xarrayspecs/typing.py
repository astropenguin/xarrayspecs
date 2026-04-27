__all__ = [
    # type aliases for Xarray dims and dtype
    "ArrayLike",
    "Dims",
    "Dtype",
    # type aliases for Xarray use
    "Attr",
    "Attrs",
    "Coord",
    "Coords",
    "Data",
    "Factory",
    "Name",
    "Vars",
]

# standard library
from collections.abc import Hashable, Mapping
from typing import Annotated, Protocol, TypeVar

# dependencies
from typespecs import ITSELF
from .core import dims, dtype, use

# type hints
TAny = TypeVar("TAny")
TDims = TypeVar("TDims", covariant=True)
TDtype = TypeVar("TDtype", covariant=True)


class ArrayLike(Protocol[TDims, TDtype]):
    pass


# type aliases for Xarray dims and dtype
Dims = Annotated[TAny, dims(ITSELF)]
Dtype = Annotated[TAny, dtype(ITSELF)]
ArrayLike = ArrayLike[Dims[TDims], Dtype[TDtype]]  # type: ignore

# type aliases for Xarray use
Attr = Annotated[TAny, use("attr")]
Attrs = Annotated[Mapping[Hashable, TAny], use("attrs")]
Coord = Annotated[ArrayLike[TDims, TDtype], use("coord")]
Coords = Annotated[Mapping[Hashable, ArrayLike[TDims, TDtype]], use("coords")]
Data = Annotated[ArrayLike[TDims, TDtype], use("data")]
Factory = Annotated[TAny, use("factory")]
Name = Annotated[TAny, use("name")]
Vars = Annotated[Mapping[Hashable, ArrayLike[TDims, TDtype]], use("vars")]
