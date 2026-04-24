# standard library
from dataclasses import dataclass
from typing import Annotated, Any, Literal

# dependencies
import numpy as np
import xarray as xr
import xarrayspecs as xs
import xarrayspecs.typing as xt
from numpy.typing import NDArray

# type hints
Lat = Literal["lat"]
Lon = Literal["lon"]


@dataclass
class Temp0(xs.AsDataArray):
    temp: Annotated[
        NDArray[Any],
        xs.use("data"),
        xs.dims("lon", "lat"),
        xs.dtype(np.float64),
        xs.attrs(long_name="Temperature", units="K"),
    ]
    lat: Annotated[
        NDArray[Any],
        xs.use("coord"),
        xs.dims("lat"),
        xs.dtype(np.float64),
        xs.attrs(long_name="Latitude", units="deg"),
    ]
    lon: Annotated[
        NDArray[Any],
        xs.use("coord"),
        xs.dims("lon"),
        xs.dtype(np.float64),
        xs.attrs(long_name="Longitude", units="deg"),
    ]
    date: Annotated[str, xs.use("attr")]


@dataclass
class Temp1(xs.AsDataArray):
    temp: Annotated[
        xt.Data[tuple[Lon, Lat], np.float64],
        xs.attrs(long_name="Temperature", units="K"),
    ]
    lat: Annotated[
        xt.Coord[Lat, np.float64],
        xs.attrs(long_name="Latitude", units="deg"),
    ]
    lon: Annotated[
        xt.Coord[Lon, np.float64],
        xs.attrs(long_name="Longitude", units="deg"),
    ]
    date: xt.Attr[str]


def test_asdataarray() -> None:
    np.random.seed(0)
    da_0 = Temp0.new(
        np.random.uniform(273, 293, size=(2, 2)),
        np.array([0, 1]),
        np.array([2, 3]),
        "2026-03-01",
    )
    np.random.seed(0)
    da_1 = Temp1.new(
        np.random.uniform(273, 293, size=(2, 2)),
        np.array([0, 1]),
        np.array([2, 3]),
        "2026-03-01",
    )
    xr.testing.assert_equal(da_0, da_1)  # type: ignore
