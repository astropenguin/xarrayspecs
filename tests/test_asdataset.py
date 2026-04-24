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
class Weather0(xs.AsDataset):
    temp: Annotated[
        NDArray[Any],
        xs.use("data"),
        xs.dims("lon", "lat"),
        xs.dtype(np.float64),
        xs.attrs(long_name="Temperature", units="K"),
    ]
    humid: Annotated[
        NDArray[Any],
        xs.use("data"),
        xs.dims("lon", "lat"),
        xs.dtype(np.float64),
        xs.attrs(long_name="Humidity", units="%"),
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
class Weather1(xs.AsDataset):
    temp: Annotated[
        xt.Data[tuple[Lon, Lat], np.float64],
        xs.attrs(long_name="Temperature", units="K"),
    ]
    humid: Annotated[
        xt.Data[tuple[Lon, Lat], np.float64],
        xs.attrs(long_name="Humidity", units="%"),
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


def test_asdataset() -> None:
    np.random.seed(0)
    ds_0 = Weather0.new(
        np.random.uniform(273, 293, size=(2, 2)),
        np.random.uniform(0, 100, size=(2, 2)),
        np.array([0, 1]),
        np.array([2, 3]),
        "2026-03-01",
    )
    np.random.seed(0)
    ds_1 = Weather1.new(
        np.random.uniform(273, 293, size=(2, 2)),
        np.random.uniform(0, 100, size=(2, 2)),
        np.array([0, 1]),
        np.array([2, 3]),
        "2026-03-01",
    )
    xr.testing.assert_equal(ds_0, ds_1)  # type: ignore
