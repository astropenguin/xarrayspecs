# standard library
from dataclasses import dataclass
from typing import Annotated, Any

# dependencies
import numpy as np
import xarrayspecs as xs
from numpy.typing import NDArray

# type hints
Temp = Annotated[
    NDArray[Any],
    xs.use("data"),
    xs.name("temp"),
    xs.dims("lon", "lat"),
    xs.dtype(np.float64),
    xs.attrs(long_name="Temperature", units="K"),
]
Humid = Annotated[
    NDArray[Any],
    xs.use("data"),
    xs.name("humid"),
    xs.dims("lon", "lat"),
    xs.dtype(np.float64),
    xs.attrs(long_name="Humidity", units="%"),
]
Lat = Annotated[
    NDArray[Any],
    xs.use("coord"),
    xs.name("lat"),
    xs.dims("lat"),
    xs.dtype(np.float64),
    xs.attrs(long_name="Latitude", units="deg"),
]
Lon = Annotated[
    NDArray[Any],
    xs.use("coord"),
    xs.name("lon"),
    xs.dims("lon"),
    xs.dtype(np.float64),
    xs.attrs(long_name="Longitude", units="deg"),
]
Date = Annotated[str, xs.use("attr"), xs.name("date")]


@dataclass
class Weathers(xs.AsDataTree):
    temp_0: Annotated[Temp, xs.node("/0")]
    temp_1: Annotated[Temp, xs.node("/1")]
    humid_0: Annotated[Humid, xs.node("/0")]
    humid_1: Annotated[Humid, xs.node("/1")]
    lat_0: Annotated[Lat, xs.node("/0")]
    lat_1: Annotated[Lat, xs.node("/1")]
    lon_0: Annotated[Lon, xs.node("/0")]
    lon_1: Annotated[Lon, xs.node("/1")]
    date_0: Annotated[Date, xs.node("/0")]
    date_1: Annotated[Date, xs.node("/1")]


def test_asdatatree() -> None:
    Weathers.new(
        np.random.uniform(273, 293, size=(2, 2)),
        np.random.uniform(273, 293, size=(2, 2)),
        np.random.uniform(0, 100, size=(2, 2)),
        np.random.uniform(0, 100, size=(2, 2)),
        np.arange(2),
        np.arange(2) + 1,
        np.arange(2),
        np.arange(2) + 1,
        "2026-03-01",
        "2026-03-01",
    )
