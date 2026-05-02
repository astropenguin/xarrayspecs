# standard library
from dataclasses import dataclass
from typing import Annotated, Any, Literal

# dependencies
import numpy as np
import xarray as xr
import xarrayspecs as xs
from numpy.typing import NDArray
from pydantic import BaseModel

# type hints
Lat = Literal["lat"]
Lon = Literal["lon"]


class CustomSet(xr.Dataset):
    __slots__ = ()


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
    factory: Annotated[type[CustomSet], xs.use("factory")] = CustomSet


@dataclass
class Weather1(xs.AsDataset):
    temp: Annotated[
        xs.Data[tuple[Lon, Lat], np.float64],
        xs.attrs(long_name="Temperature", units="K"),
    ]
    humid: Annotated[
        xs.Data[tuple[Lon, Lat], np.float64],
        xs.attrs(long_name="Humidity", units="%"),
    ]
    lat: Annotated[
        xs.Coord[Lat, np.float64],
        xs.attrs(long_name="Latitude", units="deg"),
    ]
    lon: Annotated[
        xs.Coord[Lon, np.float64],
        xs.attrs(long_name="Longitude", units="deg"),
    ]
    date: xs.Attr[str]
    factory: xs.Factory[CustomSet] = CustomSet


class Weather2(BaseModel, xs.AsDataset):
    temp: Annotated[
        xs.Data[tuple[Lon, Lat], np.float64],
        xs.attrs(long_name="Temperature", units="K"),
    ]
    humid: Annotated[
        xs.Data[tuple[Lon, Lat], np.float64],
        xs.attrs(long_name="Humidity", units="%"),
    ]
    lat: Annotated[
        xs.Coord[Lat, np.float64],
        xs.attrs(long_name="Latitude", units="deg"),
    ]
    lon: Annotated[
        xs.Coord[Lon, np.float64],
        xs.attrs(long_name="Longitude", units="deg"),
    ]
    date: xs.Attr[str]
    factory: xs.Factory[CustomSet] = CustomSet


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
    np.random.seed(0)
    ds_2 = Weather2.new(
        temp=np.random.uniform(273, 293, size=(2, 2)),
        humid=np.random.uniform(0, 100, size=(2, 2)),
        lat=np.array([0, 1]),
        lon=np.array([2, 3]),
        date="2026-03-01",
    )
    xr.testing.assert_equal(ds_0, ds_1)  # type: ignore
    xr.testing.assert_equal(ds_0, ds_2)  # type: ignore
