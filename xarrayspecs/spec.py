__all__ = [
    "Dims",
    "Dtype",
    "Type",
    "attrs",
    "dims",
    "dtype",
    "name",
    "node",
    "type",
    "use",
]

# standard library
from collections.abc import Callable, Hashable, Iterable, Mapping
from typing import Annotated, Any, Literal, TypeVar, overload

# dependencies
from typespecs import ITSELF, Spec

# type hints
T = TypeVar("T")


Dims = Annotated[T, Spec(xarray_dims=ITSELF)]
"""Type hint for Xarray dimensions."""


Dtype = Annotated[T, Spec(xarray_dtype=ITSELF)]
"""Type hint for Xarray data type."""


Type = Annotated[T, Spec(xarray_type=ITSELF)]
"""Type hint for Xarray type."""


Use = Literal[
    "attr",
    "attrs",
    "coord",
    "coords",
    "data",
    "name",
    "other",
    "type",
    "vars",
]
"""Type hint for Xarray use."""


@overload
def attrs(attrs: Mapping[Any, Any] | None, /) -> Spec: ...
@overload
def attrs(**attrs: Any) -> Spec: ...
def attrs(*args: Any, **kwargs: Any) -> Spec:
    """Returns a type specification for Xarray attributes."""
    if len(args) == 0:
        return Spec(xarray_attrs=kwargs)

    if len(args) == 1 and not kwargs:
        return Spec(xarray_attrs=args[0])

    raise ValueError("Cannot create type specification.")


@overload
def dims(dims: Iterable[Hashable] | None, /) -> Spec: ...
@overload
def dims(*dims: Hashable) -> Spec: ...
def dims(*args: Any) -> Spec:
    """Returns a type specification for Xarray dimensions."""
    if len(args) == 1:
        return Spec(xarray_dims=args[0])
    else:
        return Spec(xarray_dims=args)


def dtype(dtype: Any | None, /) -> Spec:
    """Returns a type specification for Xarray data type."""
    return Spec(xarray_dtype=dtype)


def name(name: Hashable | None, /) -> Spec:
    """Returns a type specification for Xarray name."""
    return Spec(xarray_name=name)


def node(node: str, /) -> Spec:
    """Returns a type specification for Xarray node."""
    return Spec(xarray_node=node)


def type(type: Callable[..., Any] | None, /) -> Spec:
    """Returns a type specification for Xarray type."""
    return Spec(xarray_type=type)


def use(use: Use, /) -> Spec:
    """Returns a type specification for Xarray use."""
    return Spec(xarray_use=use)
