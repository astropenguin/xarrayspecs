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
    "to_type",
    "to_vars",
]

# standard library
from collections.abc import Hashable
from typing import Any, TypeVar

# dependencies
import pandas as pd
import xarray as xr
from pandas.api.types import is_scalar
from typespecs import SpecFrame, from_annotated
from typespecs.typing import is_literal
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

        def type_(*args: Any, **kwargs: Any) -> xr.DataArray:
            if spec.xarray_type is None:
                da: Any = xr.DataArray(*args, **kwargs)
            else:
                da: Any = spec.xarray_type(*args, **kwargs)

            if spec.xarray_dtype is None:
                return da
            else:
                return da.astype(spec.xarray_dtype, copy=False)

        if spec.xarray_use == "coord":
            coords[spec.xarray_name] = type_(
                data=spec.data,
                dims=spec.xarray_dims,
                name=spec.xarray_name,
                attrs=spec.xarray_attrs,
            )
        elif spec.xarray_use == "coords":
            for name, data in spec.data.items():
                coords[name] = type_(
                    data=data,
                    dims=spec.xarray_dims,
                    name=name,
                    attrs=spec.xarray_attrs,
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


def to_dims(obj: Any, /) -> tuple[Hashable, ...] | None:
    """Convert given object to Xarray dimensions."""
    if obj is None:
        return None

    if is_literal(obj) or is_scalar(obj):
        obj = (obj,)

    if get_origin(obj) is tuple:
        obj = get_args(obj)

    return tuple(get_args(v)[0] if is_literal(v) else v for v in obj)


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

        def type_(*args: Any, **kwargs: Any) -> xr.DataArray:
            if spec.xarray_type is None:
                da: Any = xr.DataArray(*args, **kwargs)
            else:
                da: Any = spec.xarray_type(*args, **kwargs)

            if spec.xarray_dtype is None:
                return da
            else:
                return da.astype(spec.xarray_dtype, copy=False)

        if spec.xarray_use == "data":
            vars[spec.xarray_name] = type_(
                data=spec.data,
                dims=spec.xarray_dims,
                name=spec.xarray_name,
                attrs=spec.xarray_attrs,
            )
        elif spec.xarray_use == "vars":
            for name, data in spec.data.items():
                vars[name] = type_(
                    data=data,
                    dims=spec.xarray_dims,
                    name=name,
                    attrs=spec.xarray_attrs,
                )

    return vars
