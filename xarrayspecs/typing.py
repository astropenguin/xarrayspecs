__all__ = [
    # type aliases for Xarray dims, dtype, and type
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
    "Name",
    "Type",
    "Vars",
]

# standard library
from typing import Annotated, Protocol, TypeVar

# dependencies
from typespecs import ITSELF, Spec

# type hints
T = TypeVar("T")
TDims = TypeVar("TDims", covariant=True)
TDtype = TypeVar("TDtype", covariant=True)


class NDArray(Protocol[TDims, TDtype]):
    pass


# type aliases for Xarray dims, dtype, and type
Cast = Annotated[T, Spec(xarray_type=ITSELF)]
Dims = Annotated[T, Spec(xarray_dims=ITSELF)]
Dtype = Annotated[T, Spec(xarray_dtype=ITSELF)]
NDArray = NDArray[Dims[TDims], Dtype[TDtype]]  # type: ignore

# type aliases for Xarray use
Attr = Annotated[T, Spec(xarray_use="attr")]
Attrs = Annotated[T, Spec(xarray_use="attrs")]
Coord = Annotated[T, Spec(xarray_use="coord")]
Coords = Annotated[T, Spec(xarray_use="coords")]
Data = Annotated[T, Spec(xarray_use="data")]
Name = Annotated[T, Spec(xarray_use="name")]
Type = Annotated[T, Spec(xarray_use="type")]
Vars = Annotated[T, Spec(xarray_use="vars")]
