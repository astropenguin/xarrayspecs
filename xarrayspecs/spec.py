__all__ = [
    "Dims",
    "Dtype",
    "attrs",
    "cast",
    "dims",
    "dtype",
    "name",
    "node",
    "parse",
    "use",
]

# standard library
from collections.abc import Callable, Hashable, Iterable
from typing import Annotated, Any, Literal, TypeVar

# dependencies
from typespecs import ITSELF, Spec, SpecFrame, from_annotated
from typing_extensions import get_args, get_origin

# type hints
T = TypeVar("T")


Dims = Annotated[T, Spec(xarray_dims=ITSELF)]
"""Type hint for Xarray dimensions."""


Dtype = Annotated[T, Spec(xarray_dtype=ITSELF)]
"""Type hint for Xarray data type."""


Use = Literal[
    "attr",
    "attrs",
    "cast",
    "coord",
    "coords",
    "data",
    "name",
    "vars",
    "other",
]
"""Type hint for Xarray use."""


def attrs(attrs: dict[Any, Any] | None, /) -> Spec:
    """Returns a type specification for Xarray attributes."""
    return Spec(xarray_attrs=attrs)


def cast(cast: Callable[..., Any] | None, /) -> Spec:
    """Returns a type specification for Xarray cast."""
    return Spec(xarray_cast=cast)


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


def use(use: Use, /) -> Spec:
    """Returns a type specification for Xarray use."""
    return Spec(xarray_use=use)


def parse(obj: Any, /) -> SpecFrame:
    """Returns a specification DataFrame for Xarray."""
    specs = from_annotated(
        obj,
        default={
            "xarray_attrs": None,
            "xarray_cast": None,
            "xarray_dtype": None,
            "xarray_dims": None,
            "xarray_name": None,
            "xarray_node": "/",
            "xarray_use": "other",
        },
    )

    index = specs.index.to_series()
    specs["xarray_dims"] = specs["xarray_dims"].apply(to_dims)
    specs["xarray_name"] = specs["xarray_name"].fillna(index)
    return specs


def to_dims(obj: Any, /) -> tuple[str, ...] | None:
    """Convert a dimensions-like object to dimensions."""
    if obj is None:
        return None

    try:
        return (to_str(obj),)
    except TypeError:
        return tuple(map(to_str, to_tuple(obj)))


def to_str(obj: Any, /) -> str:
    """Convert a string-like object to a string."""
    if get_origin(obj) is Literal:
        return str(get_args(obj)[0])

    if isinstance(obj, str):
        return str(obj)

    raise TypeError(f"Cannot convert {obj!r} to string.")


def to_tuple(obj: Any, /) -> tuple[Any, ...]:
    """Convert a tuple-like object to a tuple."""
    if get_origin(obj) is tuple:
        return tuple(get_args(obj))

    if isinstance(obj, Iterable):
        return tuple(obj)  # type: ignore

    raise TypeError(f"Cannot convert {obj!r} to tuple.")
