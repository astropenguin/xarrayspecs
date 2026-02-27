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
    """Convert an Xarray specification to an Xarray DataArray."""
    specs = parse(obj)
    da = to_cast(specs, xr.DataArray)(to_data(specs), to_coords(specs))
    da.attrs.update(to_attrs(specs))
    da.name = to_name(specs, da.name)
    return da


def asdataset(obj: Any, /) -> xr.Dataset:
    """Convert an Xarray specification to an Xarray Dataset."""
    specs = parse(obj)
    ds = to_cast(specs, xr.Dataset)(to_vars(specs), to_coords(specs))
    ds.attrs.update(to_attrs(specs))
    return ds


def asdatatree(obj: Any, /) -> xr.DataTree:
    """Convert an Xarray specification to an Xarray DataTree."""
    specs = parse(obj)
    nodes: dict[str, xr.Dataset] = {}

    for name, group in specs.groupby("xarray_node"):
        ds = xr.Dataset(to_vars(group), to_coords(group))
        ds.attrs.update(to_attrs(group))
        nodes[name] = ds  # type: ignore

    dt = to_cast(specs, xr.DataTree).from_dict(nodes)  # type: ignore
    dt.name = to_name(specs, dt.name)
    return dt


def do_nothing(obj: Any, /) -> Any:
    """A cast that returns the input object unchanged."""
    return obj


def to_attrs(specs: pd.DataFrame, /) -> dict[Any, Any]:
    """Convert a specification DataFrame to Xarray attributes."""
    attrs: dict[Any, Any] = {}

    for _, spec in specs.iterrows():
        if spec.xarray_cast is None:
            cast = do_nothing
        else:
            cast = spec.xarray_cast

        if spec.xarray_use == "attr":
            attrs[spec.xarray_name] = cast(spec.data)
        elif spec.xarray_use == "attrs":
            for name, data in spec.data.items():
                attrs[name] = cast(data)

    return attrs


def to_cast(specs: pd.DataFrame, default: T, /) -> T:
    """Convert a specification DataFrame to an Xarray cast."""
    for _, spec in specs[::-1].iterrows():
        if spec.xarray_cast is None:
            cast = do_nothing
        else:
            cast = spec.xarray_cast

        if spec.xarray_use == "cast":
            return cast(spec.data)

    return default


def to_coords(specs: pd.DataFrame, /) -> dict[Hashable, xr.DataArray]:
    """Convert a specification DataFrame to Xarray coordinates."""
    coords: dict[Hashable, xr.DataArray] = {}

    for _, spec in specs.iterrows():
        if spec.xarray_cast is None:
            cast = xr.DataArray
        else:
            cast = spec.xarray_cast

        if spec.xarray_use == "coord":
            coords[spec.xarray_name] = cast(
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
                coords[name] = cast(
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
    """Convert a specification DataFrame to an Xarray data."""
    return next(reversed(to_vars(specs).values()))


def to_name(specs: pd.DataFrame, default: T, /) -> T:
    """Convert a specification DataFrame to an Xarray name."""
    for _, spec in specs[::-1].iterrows():
        if spec.xarray_cast is None:
            cast = do_nothing
        else:
            cast = spec.xarray_cast

        if spec.xarray_use == "name":
            return cast(spec.data)

    return default


def to_vars(specs: pd.DataFrame, /) -> dict[Hashable, xr.DataArray]:
    """Convert a specification DataFrame to Xarray data variables."""
    vars: dict[Hashable, xr.DataArray] = {}

    for _, spec in specs.iterrows():
        if spec.xarray_cast is None:
            cast = xr.DataArray
        else:
            cast = spec.xarray_cast

        if spec.xarray_use == "data":
            vars[spec.xarray_name] = cast(
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
                vars[name] = cast(
                    data=data,
                    dims=spec.xarray_dims,
                    name=name,
                    attrs=spec.xarray_attrs,
                ).astype(  # type: ignore
                    spec.xarray_dtype,
                    copy=False,
                )

    return vars
