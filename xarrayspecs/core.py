__all__ = [
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

# standard library
from builtins import type as Type
from collections.abc import Callable, Hashable, Iterable, Mapping
from typing import Any, Literal, Protocol, TypeVar, overload

# dependencies
import typespecs as ts
import xarray as xr
from readonlydict import Tuples
from typing_extensions import ParamSpec
from .convert import to_dataarray, to_dataset, to_datatree, to_specframe

# type hints
P = ParamSpec("P")
T = TypeVar("T", bound=xr.DataArray | xr.Dataset | xr.DataTree)
Use = Literal[
    "attr",
    "attrs",
    "coord",
    "coords",
    "data",
    "data_vars",
    "factory",
    "name",
]


class HasFactory(Protocol[P, T]):
    factory: Callable[..., T]

    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None: ...


class Other(Protocol[P]):

    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None: ...


class AsDataArray:
    """Mixin class for Xarray DataArray specifications."""

    @overload
    @classmethod
    def new(cls: Type[HasFactory[P, T]], *args: P.args, **kwargs: P.kwargs) -> T: ...
    @overload
    @classmethod
    def new(cls: Type[Other[P]], *args: P.args, **kwargs: P.kwargs) -> xr.DataArray: ...

    @classmethod
    def new(cls: Any, *args: Any, **kwargs: Any) -> Any:
        """Convert the Xarray specifications to an Xarray DataArray."""
        return asdataarray(cls(*args, **kwargs))


class AsDataset:
    """Mixin class for Xarray Dataset specifications."""

    @overload
    @classmethod
    def new(cls: Type[HasFactory[P, T]], *args: P.args, **kwargs: P.kwargs) -> T: ...
    @overload
    @classmethod
    def new(cls: Type[Other[P]], *args: P.args, **kwargs: P.kwargs) -> xr.Dataset: ...

    @classmethod
    def new(cls: Any, *args: Any, **kwargs: Any) -> Any:
        """Convert the Xarray specifications to an Xarray Dataset."""
        return asdataset(cls(*args, **kwargs))


class AsDataTree:
    """Mixin class for Xarray DataTree specifications."""

    @overload
    @classmethod
    def new(cls: Type[HasFactory[P, T]], *args: P.args, **kwargs: P.kwargs) -> T: ...
    @overload
    @classmethod
    def new(cls: Type[Other[P]], *args: P.args, **kwargs: P.kwargs) -> xr.DataTree: ...

    @classmethod
    def new(cls: Any, *args: Any, **kwargs: Any) -> Any:
        """Convert the Xarray specifications to an Xarray DataTree."""
        return asdatatree(cls(*args, **kwargs))


@overload
def asdataarray(obj: HasFactory[P, T], /) -> T: ...  # type: ignore
@overload
def asdataarray(obj: Other[P], /) -> xr.DataArray: ...


def asdataarray(obj: Any, /) -> Any:
    """Convert given Xarray specifications to an Xarray DataArray."""
    return to_dataarray(to_specframe(obj))


@overload
def asdataset(obj: HasFactory[P, T], /) -> T: ...  # type: ignore
@overload
def asdataset(obj: Other[P], /) -> xr.Dataset: ...


def asdataset(obj: Any, /) -> Any:
    """Convert given Xarray specifications to an Xarray Dataset."""
    return to_dataset(to_specframe(obj))


@overload
def asdatatree(obj: HasFactory[P, T], /) -> T: ...  # type: ignore
@overload
def asdatatree(obj: Other[P], /) -> xr.DataTree: ...


def asdatatree(obj: Any, /) -> Any:
    """Convert given Xarray specifications to an Xarray DataTree."""
    return to_datatree(to_specframe(obj))


@overload
def attrs(**kwargs: Any) -> ts.Spec: ...
@overload
def attrs(mapping: Mapping[str, Any], /, **kwargs: Any) -> ts.Spec: ...
@overload
def attrs(iterable: Tuples[str, Any], /, **kwargs: Any) -> ts.Spec: ...


def attrs(*args: Any, **kwargs: Any) -> ts.Spec:
    """Returns a type specification for Xarray attributes."""
    return ts.Spec(xarrayspecs_attrs=dict(*args, **kwargs))


@overload
def dims() -> ts.Spec: ...
@overload
def dims(iterable: Iterable[Hashable], /) -> ts.Spec: ...
@overload
def dims(*hashable: Hashable) -> ts.Spec: ...


def dims(*args: Any) -> ts.Spec:
    """Returns a type specification for Xarray dimensions."""
    if len(args) == 1:
        return ts.Spec(xarrayspecs_dims=args[0])
    else:
        return ts.Spec(xarrayspecs_dims=args)


def dtype(dtype: Any | None = None, /) -> ts.Spec:
    """Returns a type specification for Xarray data type."""
    return ts.Spec(xarrayspecs_dtype=dtype)


def name(name: Hashable | None = None, /) -> ts.Spec:
    """Returns a type specification for Xarray name."""
    return ts.Spec(xarrayspecs_name=name)


def node(node: str | None = None, /) -> ts.Spec:
    """Returns a type specification for Xarray node."""
    return ts.Spec(xarrayspecs_node=node)


def use(use: Use | None = None, /) -> ts.Spec:
    """Returns a type specification for Xarray use."""
    return ts.Spec(xarrayspecs_use=use)
