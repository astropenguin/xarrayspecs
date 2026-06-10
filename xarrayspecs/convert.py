__all__ = ["to_dataarray", "to_dataset", "to_datatree", "to_specframe"]

# standard library
from collections.abc import Callable, Hashable, Reversible
from enum import Enum
from typing import Any, TypeVar

# dependencies
import numpy as np
import pandas as pd
import typespecs as ts
import xarray as xr
from pandas.api.types import is_scalar
from typespecs.typing import is_literal
from typing_extensions import get_args, get_origin

# type hints
T = TypeVar("T")


class Use(str, Enum):
    ATTR = "attr"
    ATTRS = "attrs"
    COORD = "coord"
    COORDS = "coords"
    DATA = "data"
    DATA_VARS = "data_vars"
    ENCODING = "encoding"
    FACTORY = "factory"
    NAME = "name"


def to_dataarray(specs: pd.DataFrame, /) -> xr.DataArray:
    """Convert given specification DataFrame to an Xarray DataArray."""
    DataArray = last(find(specs, Use.FACTORY).values(), xr.DataArray)
    coords = find(specs, Use.COORD, Use.COORDS, variable)
    data_vars = find(specs, Use.DATA, Use.DATA_VARS, variable)

    name, (dims, data, attrs, encoding) = last(
        data_vars.items(),
        (None, (None, None, None, None)),
    )

    da = DataArray(data, coords, dims, name, attrs)
    da.attrs.update(find(specs, Use.ATTR, Use.ATTRS))
    da.encoding.update(last(find(specs, Use.ENCODING).values(), encoding or {}))
    da.name = last(find(specs, Use.NAME).values(), da.name)
    return da


def to_dataset(specs: pd.DataFrame, /) -> xr.Dataset:
    """Convert given specification DataFrame to an Xarray Dataset."""
    Dataset = last(find(specs, Use.FACTORY).values(), xr.Dataset)
    coords = find(specs, Use.COORD, Use.COORDS, variable)
    data_vars = find(specs, Use.DATA, Use.DATA_VARS, variable)

    ds = Dataset(data_vars, coords)
    ds.attrs.update(find(specs, Use.ATTR, Use.ATTRS))
    ds.encoding.update(last(find(specs, Use.ENCODING).values(), {}))
    return ds


def to_datatree(specs: pd.DataFrame, /) -> xr.DataTree:
    """Convert given specification DataFrame to an Xarray DataTree."""
    DataTree = last(find(specs, Use.FACTORY).values(), xr.DataTree)
    nodes: dict[str, xr.Dataset] = {}

    for name, group in specs.groupby("xarrayspecs_node"):
        nodes[name] = to_dataset(group)  # type: ignore

    dt = DataTree.from_dict(nodes)  # type: ignore
    dt.encoding.update(last(find(specs, Use.ENCODING).values(), {}))
    dt.name = last(find(specs, Use.NAME).values(), dt.name)
    return dt


def to_specframe(obj: Any, /) -> pd.DataFrame:
    """Convert given object to a specification DataFrame for Xarray."""
    specs = ts.from_annotated(
        obj,
        conflict={
            "xarrayspecs_attrs": "update",
            "xarrayspecs_encoding": "update",
        },
        default={
            "xarrayspecs_attrs": None,
            "xarrayspecs_dims": None,
            "xarrayspecs_dtype": None,
            "xarrayspecs_encoding": None,
            "xarrayspecs_name": None,
            "xarrayspecs_node": None,
            "xarrayspecs_use": None,
        },
    )
    index = specs.index.to_series()
    specs["xarrayspecs_name"] = specs["xarrayspecs_name"].fillna(index)
    return specs


def find(
    specs: pd.DataFrame,
    use_scalar: Use,
    use_mapping: Use | None = None,
    format: Callable[[Any, pd.Series], T] = lambda data, spec: data,
    /,
) -> dict[Hashable, T]:
    """Find items in given specification DataFrame with given Xarray use(s)."""
    items: dict[Hashable, T] = {}

    for _, spec in specs.iterrows():
        if (use := spec.xarrayspecs_use) == use_scalar:
            items[spec.xarrayspecs_name] = format(spec.data, spec)
        elif use == use_mapping and spec.data is not None:
            for name, data in spec.data.items():
                items[name] = format(data, spec)

    return items


def last(obj: Reversible[T], default: T, /) -> T:
    """Return the last item of given reversible object or the default value."""
    return next(reversed(obj), default)


def variable(data: Any, spec: pd.Series, /) -> tuple[
    tuple[Hashable, ...] | None,  # dims
    Any,  # data
    dict[Hashable, Any] | None,  # attrs
    dict[Hashable, Any] | None,  # encoding
]:
    """Format given data with given specification Series to an Xarray variable."""
    if (dims := spec.xarrayspecs_dims) is not None:
        if is_literal(dims) or is_scalar(dims):
            dims = (dims,)

        if get_origin(dims) is tuple:
            dims = get_args(dims)

        dims = tuple(get_args(v)[0] if is_literal(v) else v for v in dims)

    if (dtype := spec.xarrayspecs_dtype) is not Any and dtype is not None:
        if hasattr(data, "astype"):
            data = data.astype(dtype, copy=False)
        else:
            data = np.asarray(data, dtype=dtype)

    return dims, data, spec.xarrayspecs_attrs, spec.xarrayspecs_encoding
