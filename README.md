# Xarrayspecs

[![Release](https://img.shields.io/pypi/v/xarrayspecs?label=Release&color=cornflowerblue&style=flat-square)](https://pypi.org/project/xarrayspecs/)
[![Python](https://img.shields.io/pypi/pyversions/xarrayspecs?label=Python&color=cornflowerblue&style=flat-square)](https://pypi.org/project/xarrayspecs/)
[![Downloads](https://img.shields.io/pypi/dm/xarrayspecs?label=Downloads&color=cornflowerblue&style=flat-square)](https://pepy.tech/project/xarrayspecs)
[![Tests](https://img.shields.io/github/actions/workflow/status/astropenguin/xarrayspecs/tests.yaml?label=Tests&style=flat-square)](https://github.com/astropenguin/xarrayspecs/actions)

Xarray specifications by type hints

## Installation

```shell
pip install xarrayspecs
```

## Basic Usage

### Xarray DataArray Specifications

```python
import numpy as np
import xarrayspecs as xs
from dataclasses import dataclass
from numpy.typing import NDArray
from typing import Annotated, Any


@dataclass
class Temp(xs.AsDataArray):
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


Temp.new(
    np.random.uniform(273, 293, size=(2, 2)),
    np.array([0, 1]),
    np.array([2, 3]),
    "2026-03-01",
)
```
```
<xarray.DataArray 'temp' (lon: 2, lat: 2)> Size: 32B
array([[283.97627008, 287.30378733],
       [285.05526752, 283.89766366]])
Coordinates:
  * lon      (lon) float64 16B 2.0 3.0
  * lat      (lat) float64 16B 0.0 1.0
Attributes:
    long_name:  Temperature
    units:      K
    date:       2026-03-01
```

### Xarray Dataset Specifications

```python
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


Weather.new(
    np.random.uniform(273, 293, size=(2, 2)),
    np.random.uniform(0, 100, size=(2, 2)),
    np.array([0, 1]),
    np.array([2, 3]),
    "2026-03-01",
)
```
```
<xarray.Dataset> Size: 96B
Dimensions:  (lat: 2, lon: 2)
Coordinates:
  * lat      (lat) float64 16B 0.0 1.0
  * lon      (lon) float64 16B 2.0 3.0
Data variables:
    temp     (lon, lat) float64 32B 284.0 287.3 285.1 283.9
    humid    (lon, lat) float64 32B 42.37 64.59 43.76 89.18
Attributes:
    date:     2026-03-01
```

### Xarray DataTree Specifications

```python
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


Weathers.new(
    np.random.uniform(273, 293, size=(2, 2)),
    np.random.uniform(273, 293, size=(2, 2)),
    np.random.uniform(0, 100, size=(2, 2)),
    np.random.uniform(0, 100, size=(2, 2)),
    np.array([0, 1]),
    np.array([0, 1]),
    np.array([2, 3]),
    np.array([2, 3]),
    "2026-03-01",
    "2026-03-01",
)
```
```
<xarray.DataTree>
Group: /
├── Group: /0
│       Dimensions:  (lat: 2, lon: 2)
│       Coordinates:
│         * lat      (lat) float64 16B 0.0 1.0
│         * lon      (lon) float64 16B 2.0 3.0
│       Data variables:
│           temp     (lon, lat) float64 32B 284.0 287.3 285.1 283.9
│           humid    (lon, lat) float64 32B 96.37 38.34 79.17 52.89
│       Attributes:
│           date:     2026-03-01
└── Group: /1
        Dimensions:  (lat: 2, lon: 2)
        Coordinates:
          * lat      (lat) float64 16B 0.0 1.0
          * lon      (lon) float64 16B 2.0 3.0
        Data variables:
            temp     (lon, lat) float64 32B 281.5 285.9 281.8 290.8
            humid    (lon, lat) float64 32B 56.8 92.56 7.104 8.713
        Attributes:
            date:     2026-03-01
```
