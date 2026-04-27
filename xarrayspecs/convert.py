__all__ = [
    "to_attrs",
    "to_coords",
    "to_data",
    "to_dataarray",
    "to_dataset",
    "to_datatree",
    "to_dims",
    "to_factory",
    "to_name",
    "to_specframe",
    "to_vars",
]

# standard library
from collections.abc import Hashable
from typing import Any, TypeVar

# dependencies
import xarray as xr
from pandas.api.types import is_scalar
from typespecs import SpecFrame, from_annotated
from typespecs.typing import is_literal
from typing_extensions import get_args, get_origin

# type hints
T = TypeVar("T")


def to_attrs(specs: SpecFrame, /) -> dict[Any, Any]:
    """Convert given specification DataFrame to Xarray attributes."""
    attrs: dict[Any, Any] = {}

    for _, spec in specs.iterrows():
        if spec.xarrayspecs_use == "attr":
            attrs[spec.xarrayspecs_name] = spec.data
        elif spec.xarrayspecs_use == "attrs":
            for name, data in spec.data.items():
                attrs[name] = data

    return attrs


def to_coords(specs: SpecFrame, /) -> dict[Hashable, xr.DataArray]:
    """Convert given specification DataFrame to Xarray coordinates."""
    coords: dict[Hashable, xr.DataArray] = {}

    for _, spec in specs.iterrows():

        def factory(*args: Any, **kwargs: Any) -> xr.DataArray:
            da = xr.DataArray(*args, **kwargs)

            if (dtype := spec.xarrayspecs_dtype) is None:
                return da
            else:
                return da.astype(dtype, copy=False)  # type: ignore

        if spec.xarrayspecs_use == "coord":
            coords[spec.xarrayspecs_name] = factory(
                data=spec.data,
                dims=spec.xarrayspecs_dims,
                name=spec.xarrayspecs_name,
                attrs=spec.xarrayspecs_attrs,
            )
        elif spec.xarrayspecs_use == "coords":
            for name, data in spec.data.items():
                coords[name] = factory(
                    data=data,
                    dims=spec.xarrayspecs_dims,
                    name=name,
                    attrs=spec.xarrayspecs_attrs,
                )

    return coords


def to_data(specs: SpecFrame, /) -> xr.DataArray:
    """Convert given specification DataFrame to an Xarray data."""
    return next(reversed(to_vars(specs).values()))


def to_dataarray(specs: SpecFrame, /) -> xr.DataArray:
    """Convert given specification DataFrame to an Xarray DataArray."""
    da = to_factory(specs, xr.DataArray)(to_data(specs), to_coords(specs))
    da.attrs.update(to_attrs(specs))
    da.name = to_name(specs, da.name)
    return da


def to_dataset(specs: SpecFrame, /) -> xr.Dataset:
    """Convert given specification DataFrame to an Xarray Dataset."""
    ds = to_factory(specs, xr.Dataset)(to_vars(specs), to_coords(specs))
    ds.attrs.update(to_attrs(specs))
    return ds


def to_datatree(specs: SpecFrame, /) -> xr.DataTree:
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


def to_factory(specs: SpecFrame, default: T, /) -> T:
    """Convert given specification DataFrame to an Xarray factory."""
    for _, spec in specs[::-1].iterrows():
        if spec.xarrayspecs_use == "factory":
            return spec.data

    return default


def to_name(specs: SpecFrame, default: T, /) -> T:
    """Convert given specification DataFrame to an Xarray name."""
    for _, spec in specs[::-1].iterrows():
        if spec.xarrayspecs_use == "name":
            return spec.data

    return default


def to_specframe(obj: Any, /) -> SpecFrame:
    """Convert given object to a specification DataFrame."""
    specs = from_annotated(
        obj,
        default={
            "xarrayspecs_attrs": None,
            "xarrayspecs_dtype": None,
            "xarrayspecs_dims": None,
            "xarrayspecs_name": None,
            "xarrayspecs_node": None,
            "xarrayspecs_use": None,
        },
    )

    index = specs.index.to_series()
    specs["xarrayspecs_dims"] = specs["xarrayspecs_dims"].apply(to_dims)
    specs["xarrayspecs_name"] = specs["xarrayspecs_name"].fillna(index)
    return specs


def to_vars(specs: SpecFrame, /) -> dict[Hashable, xr.DataArray]:
    """Convert given specification DataFrame to Xarray data variables."""
    vars: dict[Hashable, xr.DataArray] = {}

    for _, spec in specs.iterrows():

        def factory(*args: Any, **kwargs: Any) -> xr.DataArray:
            da = xr.DataArray(*args, **kwargs)

            if (dtype := spec.xarrayspecs_dtype) is None:
                return da
            else:
                return da.astype(dtype, copy=False)  # type: ignore

        if spec.xarrayspecs_use == "data":
            vars[spec.xarrayspecs_name] = factory(
                data=spec.data,
                dims=spec.xarrayspecs_dims,
                name=spec.xarrayspecs_name,
                attrs=spec.xarrayspecs_attrs,
            )
        elif spec.xarrayspecs_use == "vars":
            for name, data in spec.data.items():
                vars[name] = factory(
                    data=data,
                    dims=spec.xarrayspecs_dims,
                    name=name,
                    attrs=spec.xarrayspecs_attrs,
                )

    return vars
