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
    "Factory",
    "Name",
]

# standard library
from collections.abc import Callable, Hashable, Mapping
from typing import TYPE_CHECKING, Annotated, Any, Protocol, TypeVar

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
Dims = Annotated[T, dims(ts.ITSELF)]
Dtype = Annotated[T, dtype(ts.ITSELF)]
ArrayLike = ArrayLike[Dims[TDims], Dtype[TDtype]]  # type: ignore

# type aliases for Xarray use
Attr = Annotated[T, use("attr")]
Attrs = Annotated[Mapping[Hashable, T], use("attrs")]
Coord = Annotated[ArrayLike[TDims, TDtype], use("coord")]
Coords = Annotated[Mapping[Hashable, ArrayLike[TDims, TDtype]], use("coords")]
Data = Annotated[ArrayLike[TDims, TDtype], use("data")]
DataVars = Annotated[Mapping[Hashable, ArrayLike[TDims, TDtype]], use("data_vars")]
Factory = Annotated[Callable[..., T], use("factory")]
Name = Annotated[T, use("name")]
