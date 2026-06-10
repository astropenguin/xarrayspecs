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
    "DataVars",
    "Encoding",
    "Factory",
    "Name",
]

# standard library
from collections.abc import Callable, Hashable, Mapping
from typing import TYPE_CHECKING, Annotated as Ann, Any, Protocol, TypeVar

# dependencies
import typespecs as ts
from .core import dims, dtype, use

# type hints
T = TypeVar("T")
TDims = TypeVar("TDims", covariant=True)
TDtype = TypeVar("TDtype", covariant=True)


class ArrayLike(Protocol[TDims, TDtype]):
    if not TYPE_CHECKING:

        @classmethod
        def __get_pydantic_core_schema__(cls, *args: Any, **kwargs: Any) -> Any:
            """Returns a Pydantic core schema that matches any data."""
            from pydantic_core import core_schema

            return core_schema.any_schema()


# type aliases for Xarray dims and dtype
Dims = Ann[T, dims(ts.ITSELF)]
Dtype = Ann[T, dtype(ts.ITSELF)]
ArrayLike = ArrayLike[Dims[TDims], Dtype[TDtype]]  # type: ignore

# type aliases for Xarray use
Attr = Ann[T, use("attr")]
Attrs = Ann[Mapping[Hashable, T] | None, use("attrs")]
Coord = Ann[ArrayLike[TDims, TDtype], use("coord")]
Coords = Ann[Mapping[Hashable, ArrayLike[TDims, TDtype]] | None, use("coords")]
Data = Ann[ArrayLike[TDims, TDtype], use("data")]
DataVars = Ann[Mapping[Hashable, ArrayLike[TDims, TDtype]] | None, use("data_vars")]
Encoding = Ann[Mapping[Hashable, T] | None, use("encoding")]
Factory = Ann[Callable[..., T], use("factory")]
Name = Ann[T, use("name")]
