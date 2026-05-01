__all__ = [
    "to_attrs",
    "to_coords",
    "to_data",
    "to_dataarray",
    "to_dataset",
    "to_datatree",
    "to_factory",
    "to_name",
    "to_specframe",
    "to_vars",
]

# standard library
from collections.abc import Hashable
from enum import Enum
from typing import Any, TypeVar

# dependencies
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
    FACTORY = "factory"
    NAME = "name"
    VARS = "vars"


def to_attrs(specs: ts.SpecFrame, /) -> dict[Any, Any]:
    """Convert given specification DataFrame to Xarray attributes."""
    attrs: dict[Any, Any] = {}

    for _, spec in specs.iterrows():
        if spec.xarrayspecs_use == Use.ATTR:
            attrs[spec.xarrayspecs_name] = spec.data
        elif spec.xarrayspecs_use == Use.ATTRS:
            for name, data in spec.data.items():
                attrs[name] = data

    return attrs


def to_coords(specs: ts.SpecFrame, /) -> dict[Hashable, xr.DataArray]:
    """Convert given specification DataFrame to Xarray coordinates."""
    coords: dict[Hashable, xr.DataArray] = {}

    for _, spec in specs.iterrows():

        def factory(*args: Any, **kwargs: Any) -> xr.DataArray:
            da = xr.DataArray(*args, **kwargs)

            if (dtype := spec.xarrayspecs_dtype) is None:
                return da
            else:
                return da.astype(dtype, copy=False)  # type: ignore

        if spec.xarrayspecs_use == Use.COORD:
            coords[spec.xarrayspecs_name] = factory(
                data=spec.data,
                dims=spec.xarrayspecs_dims,
                name=spec.xarrayspecs_name,
                attrs=spec.xarrayspecs_attrs,
            )
        elif spec.xarrayspecs_use == Use.COORDS:
            for name, data in spec.data.items():
                coords[name] = factory(
                    data=data,
                    dims=spec.xarrayspecs_dims,
                    name=name,
                    attrs=spec.xarrayspecs_attrs,
                )

    return coords


def to_data(specs: ts.SpecFrame, /) -> xr.DataArray:
    """Convert given specification DataFrame to an Xarray data."""
    return next(reversed(to_vars(specs).values()))


def to_dataarray(specs: ts.SpecFrame, /) -> xr.DataArray:
    """Convert given specification DataFrame to an Xarray DataArray."""
    da = to_factory(specs, xr.DataArray)(to_data(specs), to_coords(specs))
    da.attrs.update(to_attrs(specs))
    da.name = to_name(specs, da.name)
    return da


def to_dataset(specs: ts.SpecFrame, /) -> xr.Dataset:
    """Convert given specification DataFrame to an Xarray Dataset."""
    ds = to_factory(specs, xr.Dataset)(to_vars(specs), to_coords(specs))
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


def to_dims(obj: Any, /) -> tuple[Hashable, ...] | None:
    """Convert given object to Xarray dimensions."""
    if obj is None:
        return None

    if is_literal(obj) or is_scalar(obj):
        obj = (obj,)

    if get_origin(obj) is tuple:
        obj = get_args(obj)

    return tuple(get_args(v)[0] if is_literal(v) else v for v in obj)


def to_dtype(obj: Any, /) -> Any | None:
    """Convert given object to an Xarray dtype."""
    return None if obj is Any else obj


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
    specs["xarrayspecs_dims"] = specs.xarrayspecs_dims.apply(to_dims)
    specs["xarrayspecs_dtype"] = specs.xarrayspecs_dtype.apply(to_dtype)
    specs["xarrayspecs_name"] = specs.xarrayspecs_name.fillna(index)
    return specs


def to_vars(specs: ts.SpecFrame, /) -> dict[Hashable, xr.DataArray]:
    """Convert given specification DataFrame to Xarray data variables."""
    vars: dict[Hashable, xr.DataArray] = {}

    for _, spec in specs.iterrows():

        def factory(*args: Any, **kwargs: Any) -> xr.DataArray:
            da = xr.DataArray(*args, **kwargs)

            if (dtype := spec.xarrayspecs_dtype) is None:
                return da
            else:
                return da.astype(dtype, copy=False)  # type: ignore

        if spec.xarrayspecs_use == Use.DATA:
            vars[spec.xarrayspecs_name] = factory(
                data=spec.data,
                dims=spec.xarrayspecs_dims,
                name=spec.xarrayspecs_name,
                attrs=spec.xarrayspecs_attrs,
            )
        elif spec.xarrayspecs_use == Use.VARS:
            for name, data in spec.data.items():
                vars[name] = factory(
                    data=data,
                    dims=spec.xarrayspecs_dims,
                    name=name,
                    attrs=spec.xarrayspecs_attrs,
                )

    return vars
