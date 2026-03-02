__all__ = [
    "AsDataArray",
    "AsDataset",
    "AsDataTree",
    "asdataarray",
    "asdataset",
    "asdatatree",
]

# standard library
from collections.abc import Callable
from typing import Any, Protocol, TypeVar, overload

# dependencies
import xarray as xr
from typing_extensions import ParamSpec
from .convert import to_dataarray, to_dataset, to_datatree, to_specframe

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
        """Convert the Xarray specifications to an Xarray DataArray."""
        return asdataarray(cls(*args, **kwargs))


class AsDataset:
    """Mixin class for Xarray Dataset specifications."""

    type_: Callable[..., xr.Dataset]

    @classmethod
    def new(cls: type[HasType[P, T]], *args: P.args, **kwargs: P.kwargs) -> T:
        """Convert the Xarray specifications to an Xarray Dataset."""
        return asdataset(cls(*args, **kwargs))


class AsDataTree:
    """Mixin class for Xarray DataTree specifications."""

    type_: Callable[..., xr.DataTree]

    @classmethod
    def new(cls: type[HasType[P, T]], *args: P.args, **kwargs: P.kwargs) -> T:
        """Convert the Xarray specifications to an Xarray DataTree."""
        return asdatatree(cls(*args, **kwargs))


@overload
def asdataarray(obj: HasType[P, T], /) -> T: ...  # type: ignore
@overload
def asdataarray(obj: Any, /) -> xr.DataArray: ...
def asdataarray(obj: Any, /) -> Any:
    """Convert given Xarray specifications to an Xarray DataArray."""
    return to_dataarray(to_specframe(obj))


@overload
def asdataset(obj: HasType[P, T], /) -> T: ...  # type: ignore
@overload
def asdataset(obj: Any, /) -> xr.Dataset: ...
def asdataset(obj: Any, /) -> Any:
    """Convert given Xarray specifications to an Xarray Dataset."""
    return to_dataset(to_specframe(obj))


@overload
def asdatatree(obj: HasType[P, T], /) -> T: ...  # type: ignore
@overload
def asdatatree(obj: Any, /) -> xr.DataTree: ...
def asdatatree(obj: Any, /) -> Any:
    """Convert given Xarray specifications to an Xarray DataTree."""
    return to_datatree(to_specframe(obj))
