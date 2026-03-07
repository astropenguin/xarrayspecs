# standard library
from dataclasses import dataclass
from typing import Annotated, Any

# dependencies
import numpy as np
import xarrayspecs as xs
from numpy.typing import NDArray


@dataclass
class Weather(xs.AsDataset):
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


def test_asdataset() -> None:
    Weather.new(
        np.random.uniform(273, 293, size=(2, 2)),
        np.random.uniform(0, 100, size=(2, 2)),
        np.array([0, 1]),
        np.array([2, 3]),
        "2026-03-01",
    )
