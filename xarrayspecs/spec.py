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
from collections.abc import Callable, Hashable, Iterable
from typing import Annotated, Any, Literal, TypeVar

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


def attrs(attrs: dict[Any, Any] | None, /) -> Spec:
    """Returns a type specification for Xarray attributes."""
    return Spec(xarray_attrs=attrs)


def dims(dims: Iterable[str] | str | None, /) -> Spec:
    """Returns a type specification for Xarray dimensions."""
    return Spec(xarray_dims=dims)


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
