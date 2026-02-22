__all__ = ["asarray", "asset", "astree"]

# standard library
from collections.abc import Hashable
from typing import Any

# dependencies
import pandas as pd
import xarray as xr
from .spec import parse


def asarray(obj: Any, /) -> xr.DataArray:
    """Convert an xarray specification to an xarray DataArray."""
    specs = parse(obj)
    da = xr.DataArray(
        data=next(iter(to_vars(specs).values())),
        coords=to_coords(specs),
    )
    da.attrs.update(to_attrs(specs))
    return da


def asset(obj: Any, /) -> xr.Dataset:
    """Convert an xarray specification to an xarray Dataset."""
    specs = parse(obj)
    ds = xr.Dataset(
        data_vars=to_vars(specs),
        coords=to_coords(specs),
    )
    ds.attrs.update(to_attrs(specs))
    return ds


def astree(obj: Any, /) -> xr.DataTree:
    """Convert an xarray specification to an xarray DataTree."""
    specs = parse(obj)
    nodes: dict[str, xr.Dataset] = {}

    for node, subspecs in specs.groupby("xarray_node"):
        ds = xr.Dataset(
            data_vars=to_vars(subspecs),
            coords=to_coords(subspecs),
        )
        ds.attrs.update(to_attrs(subspecs))
        nodes[node] = ds  # type: ignore

    return xr.DataTree.from_dict(nodes)  # type: ignore


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
