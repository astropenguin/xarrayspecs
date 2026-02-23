__all__ = ["asdataarray", "asdataset", "asdatatree"]

# standard library
from collections.abc import Hashable
from typing import Any, TypeVar

# dependencies
import pandas as pd
import xarray as xr
from .spec import parse

# type hints
T = TypeVar("T")


def asdataarray(obj: Any, /) -> xr.DataArray:
    """Convert an xarray specification to an xarray DataArray."""
    specs = parse(obj)
    da = to_factory(specs, xr.DataArray)(to_data(specs), to_coords(specs))
    da.attrs.update(to_attrs(specs))
    da.name = to_name(specs, da.name)
    return da


def asdataset(obj: Any, /) -> xr.Dataset:
    """Convert an xarray specification to an xarray Dataset."""
    specs = parse(obj)
    ds = to_factory(specs, xr.Dataset)(to_vars(specs), to_coords(specs))
    ds.attrs.update(to_attrs(specs))
    return ds


def asdatatree(obj: Any, /) -> xr.DataTree:
    """Convert an xarray specification to an xarray DataTree."""
    specs = parse(obj)
    nodes: dict[str, xr.Dataset] = {}

    for name, group in specs.groupby("xarray_node"):
        ds = xr.Dataset(to_vars(group), to_coords(group))
        ds.attrs.update(to_attrs(group))
        nodes[name] = ds  # type: ignore

    dt = to_factory(specs, xr.DataTree).from_dict(nodes)  # type: ignore
    dt.name = to_name(specs, dt.name)
    return dt


def to_attrs(specs: pd.DataFrame, /) -> dict[Any, Any]:
    """Convert a specification DataFrame to xarray attributes."""
    attrs: dict[Any, Any] = {}

    for _, spec in specs.iterrows():
        if spec.xarray_use == "attr":
            attrs[spec.xarray_name] = spec.data
        elif spec.xarray_use == "attrs":
            attrs.update(spec.data)

    return attrs


def to_coords(specs: pd.DataFrame, /) -> dict[Hashable, xr.DataArray]:
    """Convert a specification DataFrame to xarray coordinates."""
    coords: dict[Hashable, xr.DataArray] = {}

    for _, spec in specs.iterrows():
        if spec.xarray_use == "coord":
            coords[spec.xarray_name] = xr.DataArray(
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
                coords[name] = xr.DataArray(
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
    """Convert a specification DataFrame to an xarray data."""
    return next(reversed(to_vars(specs).values()))


def to_factory(specs: pd.DataFrame, default: T, /) -> T:
    """Convert a specification DataFrame to an xarray factory."""
    for _, spec in specs[::-1].iterrows():
        if spec.xarray_use == "factory":
            return spec.data

    return default


def to_name(specs: pd.DataFrame, default: T, /) -> T:
    """Convert a specification DataFrame to an xarray name."""
    for _, spec in specs[::-1].iterrows():
        if spec.xarray_use == "name":
            return spec.data

    return default


def to_vars(specs: pd.DataFrame, /) -> dict[Hashable, xr.DataArray]:
    """Convert a specification DataFrame to xarray data variables."""
    vars: dict[Hashable, xr.DataArray] = {}

    for _, spec in specs.iterrows():
        if spec.xarray_use == "data":
            vars[spec.xarray_name] = xr.DataArray(
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
                vars[name] = xr.DataArray(
                    data=data,
                    dims=spec.xarray_dims,
                    name=name,
                    attrs=spec.xarray_attrs,
                ).astype(  # type: ignore
                    spec.xarray_dtype,
                    copy=False,
                )

    return vars
