__all__ = [
    "to_attrs",
    "to_coords",
    "to_data",
    "to_dataarray",
    "to_dataset",
    "to_datatree",
    "to_dims",
    "to_name",
    "to_specframe",
    "to_str",
    "to_tuple",
    "to_type",
    "to_vars",
]

# standard library
from collections.abc import Hashable, Iterable
from typing import Any, Literal, TypeVar

# dependencies
import pandas as pd
import xarray as xr
from typespecs import SpecFrame, from_annotated
from typing_extensions import get_args, get_origin

# type hints
T = TypeVar("T")


def to_attrs(specs: pd.DataFrame, /) -> dict[Any, Any]:
    """Convert given specification DataFrame to Xarray attributes."""
    attrs: dict[Any, Any] = {}

    for _, spec in specs.iterrows():
        if spec.xarray_type is None:
            type_ = lambda data: data  # type: ignore
        else:
            type_ = spec.xarray_type

        if spec.xarray_use == "attr":
            attrs[spec.xarray_name] = type_(spec.data)
        elif spec.xarray_use == "attrs":
            for name, data in spec.data.items():
                attrs[name] = type_(data)

    return attrs


def to_coords(specs: pd.DataFrame, /) -> dict[Hashable, xr.DataArray]:
    """Convert given specification DataFrame to Xarray coordinates."""
    coords: dict[Hashable, xr.DataArray] = {}

    for _, spec in specs.iterrows():
        if spec.xarray_type is None:
            type_ = xr.DataArray
        else:
            type_ = spec.xarray_type

        if spec.xarray_use == "coord":
            coords[spec.xarray_name] = type_(
                data=spec.data,
                dims=spec.xarray_dims,
                name=spec.xarray_name,
                attrs=spec.xarray_attrs,
            ).astype(  # type: ignore
                spec.xarray_dtype,
                copy=False,
            )
        elif spec.xarray_use == "coords":
            for name, data in spec.data.items():
                coords[name] = type_(
                    data=data,
                    dims=spec.xarray_dims,
                    name=name,
                    attrs=spec.xarray_attrs,
                ).astype(  # type: ignore
                    spec.xarray_dtype,
                    copy=False,
                )

    return coords


def to_data(specs: pd.DataFrame, /) -> xr.DataArray:
    """Convert given specification DataFrame to an Xarray data."""
    return next(reversed(to_vars(specs).values()))


def to_dataarray(specs: pd.DataFrame, /) -> xr.DataArray:
    """Convert given specification DataFrame to an Xarray DataArray."""
    da = to_type(specs, xr.DataArray)(to_data(specs), to_coords(specs))
    da.attrs.update(to_attrs(specs))
    da.name = to_name(specs, da.name)
    return da


def to_dataset(specs: pd.DataFrame, /) -> xr.Dataset:
    """Convert given specification DataFrame to an Xarray Dataset."""
    ds = to_type(specs, xr.Dataset)(to_vars(specs), to_coords(specs))
    ds.attrs.update(to_attrs(specs))
    return ds


def to_datatree(specs: pd.DataFrame, /) -> xr.DataTree:
    """Convert given specification DataFrame to an Xarray DataTree."""
    nodes: dict[str, xr.Dataset] = {}

    for name, group in specs.groupby("xarray_node"):
        ds = xr.Dataset(to_vars(group), to_coords(group))
        ds.attrs.update(to_attrs(group))
        nodes[name] = ds  # type: ignore

    dt = to_type(specs, xr.DataTree).from_dict(nodes)  # type: ignore
    dt.name = to_name(specs, dt.name)
    return dt


def to_dims(obj: Any, /) -> tuple[str, ...] | None:
    """Convert given dimensions-like object to dimensions."""
    if obj is None:
        return None

    try:
        return (to_str(obj),)
    except TypeError:
        return tuple(map(to_str, to_tuple(obj)))


def to_name(specs: pd.DataFrame, default: T, /) -> T:
    """Convert given specification DataFrame to an Xarray name."""
    for _, spec in specs[::-1].iterrows():
        if spec.xarray_type is None:
            type_ = lambda data: data  # type: ignore
        else:
            type_ = spec.xarray_type

        if spec.xarray_use == "name":
            return type_(spec.data)  # type: ignore

    return default


def to_specframe(obj: Any, /) -> SpecFrame:
    """Convert given object to a specification DataFrame."""
    specs = from_annotated(
        obj,
        default={
            "xarray_attrs": None,
            "xarray_dtype": None,
            "xarray_dims": None,
            "xarray_name": None,
            "xarray_node": "/",
            "xarray_type": None,
            "xarray_use": "other",
        },
    )

    index = specs.index.to_series()
    specs["xarray_dims"] = specs["xarray_dims"].apply(to_dims)
    specs["xarray_name"] = specs["xarray_name"].fillna(index)
    return specs


def to_str(obj: Any, /) -> str:
    """Convert given string-like object to a string."""
    if get_origin(obj) is Literal:
        return str(get_args(obj)[0])

    if isinstance(obj, str):
        return str(obj)

    raise TypeError(f"Cannot convert {obj!r} to string.")


def to_tuple(obj: Any, /) -> tuple[Any, ...]:
    """Convert given tuple-like object to a tuple."""
    if get_origin(obj) is tuple:
        return tuple(get_args(obj))

    if isinstance(obj, Iterable):
        return tuple(obj)  # type: ignore

    raise TypeError(f"Cannot convert {obj!r} to tuple.")


def to_type(specs: pd.DataFrame, default: T, /) -> T:
    """Convert given specification DataFrame to an Xarray type."""
    for _, spec in specs[::-1].iterrows():
        if spec.xarray_type is None:
            type_ = lambda data: data  # type: ignore
        else:
            type_ = spec.xarray_type

        if spec.xarray_use == "type":
            return type_(spec.data)  # type: ignore

    return default


def to_vars(specs: pd.DataFrame, /) -> dict[Hashable, xr.DataArray]:
    """Convert given specification DataFrame to Xarray data variables."""
    vars: dict[Hashable, xr.DataArray] = {}

    for _, spec in specs.iterrows():
        if spec.xarray_type is None:
            type_ = xr.DataArray
        else:
            type_ = spec.xarray_type

        if spec.xarray_use == "data":
            vars[spec.xarray_name] = type_(
                data=spec.data,
                dims=spec.xarray_dims,
                name=spec.xarray_name,
                attrs=spec.xarray_attrs,
            ).astype(  # type: ignore
                spec.xarray_dtype,
                copy=False,
            )
        elif spec.xarray_use == "vars":
            for name, data in spec.data.items():
                vars[name] = type_(
                    data=data,
                    dims=spec.xarray_dims,
                    name=name,
                    attrs=spec.xarray_attrs,
                ).astype(  # type: ignore
                    spec.xarray_dtype,
                    copy=False,
                )

    return vars
