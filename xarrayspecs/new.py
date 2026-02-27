__all__ = ["AsDataArray", "AsDataset", "AsDataTree"]

# standard library
from typing import Callable
from typing import Protocol, TypeVar

# dependencies
import xarray as xr
from typing_extensions import ParamSpec
from .api import asdataarray, asdataset, asdatatree

# type hints
P = ParamSpec("P")
T = TypeVar("T")


class HasCast(Protocol[P, T]):
    cast_: Callable[..., T]

    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None: ...


class AsDataArray:
    """Mixin class for Xarray DataArray specifications."""

    cast_: Callable[..., xr.DataArray]

    @classmethod
    def new(cls: type[HasCast[P, T]], *args: P.args, **kwargs: P.kwargs) -> T:
        """Convert the Xarray specification to an Xarray DataArray."""
        return asdataarray(cls(*args, **kwargs))


class AsDataset:
    """Mixin class for Xarray Dataset specifications."""

    cast_: Callable[..., xr.Dataset]

    @classmethod
    def new(cls: type[HasCast[P, T]], *args: P.args, **kwargs: P.kwargs) -> T:
        """Convert the Xarray specification to an Xarray Dataset."""
        return asdataset(cls(*args, **kwargs))


class AsDataTree:
    """Mixin class for Xarray DataTree specifications."""

    cast_: Callable[..., xr.DataTree]

    @classmethod
    def new(cls: type[HasCast[P, T]], *args: P.args, **kwargs: P.kwargs) -> T:
        """Convert the Xarray specification to an Xarray DataTree."""
        return asdatatree(cls(*args, **kwargs))
