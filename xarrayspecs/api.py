__all__ = ["asdataarray", "asdataset", "asdatatree"]

# standard library
from collections.abc import Callable, Hashable
from typing import Any, Protocol, TypeVar, overload

# dependencies
import pandas as pd
import xarray as xr
from .spec import parse

# type hints
T = TypeVar("T")


class HasType(Protocol[T]):
    type_: Callable[..., T]


@overload
def asdataarray(obj: HasType[T], /) -> T: ...  # type: ignore
@overload
def asdataarray(obj: Any, /) -> xr.DataArray: ...
def asdataarray(obj: Any, /) -> Any:
    """Convert given Xarray specifications to an Xarray DataArray."""
    specs = parse(obj)
    da = to_type(specs, xr.DataArray)(to_data(specs), to_coords(specs))
    da.attrs.update(to_attrs(specs))
    da.name = to_name(specs, da.name)
    return da


@overload
def asdataset(obj: HasType[T], /) -> T: ...  # type: ignore
@overload
def asdataset(obj: Any, /) -> xr.Dataset: ...
def asdataset(obj: Any, /) -> Any:
    """Convert given Xarray specifications to an Xarray Dataset."""
    specs = parse(obj)
    ds = to_type(specs, xr.Dataset)(to_vars(specs), to_coords(specs))
    ds.attrs.update(to_attrs(specs))
    return ds


@overload
def asdatatree(obj: HasType[T], /) -> T: ...  # type: ignore
@overload
def asdatatree(obj: Any, /) -> xr.DataTree: ...
def asdatatree(obj: Any, /) -> Any:
    """Convert given Xarray specifications to an Xarray DataTree."""
    specs = parse(obj)
    nodes: dict[str, xr.Dataset] = {}

    for name, group in specs.groupby("xarray_node"):
        ds = xr.Dataset(to_vars(group), to_coords(group))
        ds.attrs.update(to_attrs(group))
        nodes[name] = ds  # type: ignore

    dt = to_type(specs, xr.DataTree).from_dict(nodes)  # type: ignore
    dt.name = to_name(specs, dt.name)
    return dt


def to_attrs(specs: pd.DataFrame, /) -> dict[Any, Any]:
    """Convert a specification DataFrame to Xarray attributes."""
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
    """Convert a specification DataFrame to Xarray coordinates."""
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
    """Convert a specification DataFrame to an Xarray data."""
    return next(reversed(to_vars(specs).values()))


def to_name(specs: pd.DataFrame, default: T, /) -> T:
    """Convert a specification DataFrame to an Xarray name."""
    for _, spec in specs[::-1].iterrows():
        if spec.xarray_type is None:
            type_ = lambda data: data  # type: ignore
        else:
            type_ = spec.xarray_type

        if spec.xarray_use == "name":
            return type_(spec.data)  # type: ignore

    return default


def to_type(specs: pd.DataFrame, default: T, /) -> T:
    """Convert a specification DataFrame to an Xarray type."""
    for _, spec in specs[::-1].iterrows():
        if spec.xarray_type is None:
            type_ = lambda data: data  # type: ignore
        else:
            type_ = spec.xarray_type

        if spec.xarray_use == "type":
            return type_(spec.data)  # type: ignore

    return default


def to_vars(specs: pd.DataFrame, /) -> dict[Hashable, xr.DataArray]:
    """Convert a specification DataFrame to Xarray data variables."""
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
