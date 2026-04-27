__all__ = [
    # type aliases for Xarray dims and (d)type
    "Cast",
    "Dims",
    "Dtype",
    "NDArray",
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
from .core import dims, dtype, factory, use

# type hints
TAny = TypeVar("TAny")
TDims = TypeVar("TDims", covariant=True)
TDtype = TypeVar("TDtype", covariant=True)


class NDArray(Protocol[TDims, TDtype]):
    pass


# type aliases for Xarray dims and (d)type
Cast = Annotated[TAny, factory(ITSELF)]
Dims = Annotated[TAny, dims(ITSELF)]
Dtype = Annotated[TAny, dtype(ITSELF)]
NDArray = NDArray[Dims[TDims], Dtype[TDtype]]  # type: ignore

# type aliases for Xarray use
Attr = Annotated[TAny, use("attr")]
Attrs = Annotated[Mapping[Hashable, TAny], use("attrs")]
Coord = Annotated[NDArray[TDims, TDtype], use("coord")]
Coords = Annotated[Mapping[Hashable, NDArray[TDims, TDtype]], use("coords")]
Data = Annotated[NDArray[TDims, TDtype], use("data")]
Factory = Annotated[TAny, use("factory")]
Name = Annotated[TAny, use("name")]
Vars = Annotated[Mapping[Hashable, NDArray[TDims, TDtype]], use("vars")]
