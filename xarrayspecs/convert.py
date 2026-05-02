__all__ = [
    "to_attrs",
    "to_dataarray",
    "to_dataset",
    "to_datatree",
    "to_factory",
    "to_name",
    "to_specframe",
    "to_variables",
]

# standard library
from collections.abc import Hashable
from enum import Enum
from typing import Any, TypeVar

# dependencies
import numpy as np
import typespecs as ts
import xarray as xr
from pandas.api.types import is_scalar
from typespecs.typing import is_literal
from typing_extensions import get_args, get_origin

# type hints
T = TypeVar("T")
Attrs = dict[Hashable, Any]
Dims = tuple[Hashable, ...] | None
Dtype = Any | None
Variable = tuple[Dims, Any, Attrs]


class Use(str, Enum):
    ATTR = "attr"
    ATTRS = "attrs"
    COORD = "coord"
    COORDS = "coords"
    DATA = "data"
    FACTORY = "factory"
    NAME = "name"
    VARS = "vars"


def astype(obj: Any, dtype: Dtype, /) -> Any:
    """Convert given object to given dtype."""
    if dtype is Any or dtype is None:
        return obj

    if hasattr(obj, "astype"):
        return obj.astype(dtype, copy=False)
    else:
        return np.asarray(obj, dtype=dtype)


def dims(obj: Any, /) -> Dims:
    """Convert given object to Xarray dimensions."""
    if obj is None:
        return None

    if is_literal(obj) or is_scalar(obj):
        obj = (obj,)

    if get_origin(obj) is tuple:
        obj = get_args(obj)

    return tuple(get_args(v)[0] if is_literal(v) else v for v in obj)


def to_attrs(specs: ts.SpecFrame, /) -> Attrs:
    """Convert given specification DataFrame to Xarray attributes."""
    attrs: Attrs = {}

    for _, spec in specs.iterrows():
        if spec.xarrayspecs_use == Use.ATTR:
            attrs[spec.xarrayspecs_name] = spec.data
        elif spec.xarrayspecs_use == Use.ATTRS:
            for name, data in spec.data.items():
                attrs[name] = data

    return attrs


def to_dataarray(specs: ts.SpecFrame, /) -> xr.DataArray:
    """Convert given specification DataFrame to an Xarray DataArray."""
    coords = to_variables(specs, Use.COORD, Use.COORDS)
    data_vars = to_variables(specs, Use.DATA, Use.VARS)
    name, (dims, data, attrs) = next(reversed(data_vars.items()))

    da = to_factory(specs, xr.DataArray)(data, coords, dims, name, attrs)
    da.attrs.update(to_attrs(specs))
    da.name = to_name(specs, da.name)
    return da


def to_dataset(specs: ts.SpecFrame, /) -> xr.Dataset:
    """Convert given specification DataFrame to an Xarray Dataset."""
    coords = to_variables(specs, Use.COORD, Use.COORDS)
    data_vars = to_variables(specs, Use.DATA, Use.VARS)

    ds = to_factory(specs, xr.Dataset)(data_vars, coords)
    ds.attrs.update(to_attrs(specs))
    return ds


def to_datatree(specs: ts.SpecFrame, /) -> xr.DataTree:
    """Convert given specification DataFrame to an Xarray DataTree."""
    nodes: dict[str, xr.Dataset] = {}

    for name, group in specs.groupby("xarrayspecs_node"):
        nodes[name] = to_dataset(group)  # type: ignore

    dt = to_factory(specs, xr.DataTree).from_dict(nodes)  # type: ignore
    dt.name = to_name(specs, dt.name)
    return dt


def to_factory(specs: ts.SpecFrame, default: T, /) -> T:
    """Convert given specification DataFrame to an Xarray factory."""
    for _, spec in specs[::-1].iterrows():
        if spec.xarrayspecs_use == Use.FACTORY:
            return spec.data

    return default


def to_name(specs: ts.SpecFrame, default: T, /) -> T:
    """Convert given specification DataFrame to an Xarray name."""
    for _, spec in specs[::-1].iterrows():
        if spec.xarrayspecs_use == Use.NAME:
            return spec.data

    return default


def to_specframe(obj: Any, /) -> ts.SpecFrame:
    """Convert given object to a specification DataFrame for Xarray."""
    specs = ts.from_annotated(
        obj,
        default=dict(
            xarrayspecs_attrs=None,
            xarrayspecs_dtype=None,
            xarrayspecs_dims=None,
            xarrayspecs_name=None,
            xarrayspecs_node=None,
            xarrayspecs_use=None,
        ),
    )

    index = specs.index.to_series()
    specs["xarrayspecs_name"] = specs.xarrayspecs_name.fillna(index)
    return specs


def to_variables(
    specs: ts.SpecFrame,
    use_single: Use,
    use_multiple: Use,
    /,
) -> dict[Hashable, Variable]:
    """Convert given specification DataFrame to Xarray variables."""
    variables: dict[Hashable, Variable] = {}

    for _, spec in specs.iterrows():
        if spec.xarrayspecs_use == use_single:
            variables[spec.xarrayspecs_name] = (
                dims(spec.xarrayspecs_dims),
                astype(spec.data, spec.xarrayspecs_dtype),
                spec.xarrayspecs_attrs,
            )
        elif spec.xarrayspecs_use == use_multiple:
            for name, data in spec.data.items():
                variables[name] = (
                    dims(spec.xarrayspecs_dims),
                    astype(data, spec.xarrayspecs_dtype),
                    spec.xarrayspecs_attrs,
                )

    return variables
