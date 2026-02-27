__all__ = ["AsDataArray", "AsDataset", "AsDataTree"]

# standard library
from collections.abc import Callable
from typing import Protocol, TypeVar

# dependencies
import xarray as xr
from typing_extensions import ParamSpec
from .api import asdataarray, asdataset, asdatatree

# type hints
P = ParamSpec("P")
T = TypeVar("T")


class HasType(Protocol[P, T]):
    type_: Callable[..., T]

    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None: ...


class AsDataArray:
    """Mixin class for Xarray DataArray specifications."""

    type_: Callable[..., xr.DataArray]

    @classmethod
    def new(cls: type[HasType[P, T]], *args: P.args, **kwargs: P.kwargs) -> T:
        """Convert the Xarray specification to an Xarray DataArray."""
        return asdataarray(cls(*args, **kwargs))


class AsDataset:
    """Mixin class for Xarray Dataset specifications."""

    type_: Callable[..., xr.Dataset]

    @classmethod
    def new(cls: type[HasType[P, T]], *args: P.args, **kwargs: P.kwargs) -> T:
        """Convert the Xarray specification to an Xarray Dataset."""
        return asdataset(cls(*args, **kwargs))


class AsDataTree:
    """Mixin class for Xarray DataTree specifications."""

    type_: Callable[..., xr.DataTree]

    @classmethod
    def new(cls: type[HasType[P, T]], *args: P.args, **kwargs: P.kwargs) -> T:
        """Convert the Xarray specification to an Xarray DataTree."""
        return asdatatree(cls(*args, **kwargs))
