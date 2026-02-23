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

### Create an Xarray specification

```python
import numpy as np
import xarrayspecs as xs
from dataclasses import dataclass
from numpy.typing import NDArray
from typing import Annotated, Any


@dataclass
class Weather:
    temp: Annotated[
        NDArray[Any],
        xs.use("data"),
        xs.dims(["lon", "lat"]),
        xs.dtype(np.float64),
        xs.attrs({"long_name": "Temperature", "units": "K"}),
    ]
    wind: Annotated[
        NDArray[Any],
        xs.use("data"),
        xs.dims(["lon", "lat"]),
        xs.dtype(np.float64),
        xs.attrs({"long_name": "Wind speed", "units": "m/s"}),
    ]
    lat: Annotated[
        NDArray[Any],
        xs.use("coord"),
        xs.dims("lat"),
        xs.dtype(np.float64),
        xs.attrs({"long_name": "Latitude", "units": "deg"}),
    ]
    lon: Annotated[
        NDArray[Any],
        xs.use("coord"),
        xs.dims("lon"),
        xs.dtype(np.float64),
        xs.attrs({"long_name": "Longitude", "units": "deg"}),
    ]
    location: Annotated[str, xs.use("attr")] = "Tokyo"


weather = Weather(
    np.random.uniform(273, 293, size=(2, 2)),
    np.random.uniform(0, 10, size=(2, 2)),
    np.array([0, 1]),
    np.array([2, 3]),
)
```

### Create a DataArray from the specification

```python
print(xs.asdataarray(weather))
```
```
<xarray.DataArray 'wind' (lon: 2, lat: 2)> Size: 32B
array([[4.23654799, 6.45894113],
       [4.37587211, 8.91773001]])
Coordinates:
  * lon      (lon) float64 16B 2.0 3.0
  * lat      (lat) float64 16B 0.0 1.0
Attributes:
    long_name:  Wind speed
    units:      m/s
    location:   Tokyo
```

### Create a Dataset from the specification

```python
print(xs.asdataset(weather))
```
```
<xarray.Dataset> Size: 96B
Dimensions:  (lat: 2, lon: 2)
Coordinates:
  * lat      (lat) float64 16B 0.0 1.0
  * lon      (lon) float64 16B 2.0 3.0
Data variables:
    temp     (lon, lat) float64 32B 284.0 287.3 285.1 283.9
    wind     (lon, lat) float64 32B 4.237 6.459 4.376 8.918
Attributes:
    location:  Tokyo
```

### Create a DataTree from the specification

```python
print(xs.asdatatree(weather))
```
```
<xarray.DataTree>
Group: /
    Dimensions:  (lat: 2, lon: 2)
    Coordinates:
      * lat      (lat) float64 16B 0.0 1.0
      * lon      (lon) float64 16B 2.0 3.0
    Data variables:
        temp     (lon, lat) float64 32B 284.0 287.3 285.1 283.9
        wind     (lon, lat) float64 32B 4.237 6.459 4.376 8.918
    Attributes:
        location:  Tokyo
```

## Advanced Usage

### Check the parsed specification

```python
print(xs.parse(weather))
```
```
                                                       data                                               type                                 xarray_attrs xarray_dims             xarray_dtype xarray_use xarray_node xarray_name
temp      [[283.9762700785465, 287.3037873274484], [285....  numpy.ndarray[tuple[typing.Any, ...], numpy.dt...   {'long_name': 'Temperature', 'units': 'K'}  (lon, lat)  <class 'numpy.float64'>       data           /        temp
wind      [[4.236547993389047, 6.458941130666561], [4.37...  numpy.ndarray[tuple[typing.Any, ...], numpy.dt...  {'long_name': 'Wind speed', 'units': 'm/s'}  (lon, lat)  <class 'numpy.float64'>       data           /        wind
lat                                                  [0, 1]  numpy.ndarray[tuple[typing.Any, ...], numpy.dt...    {'long_name': 'Latitude', 'units': 'deg'}      (lat,)  <class 'numpy.float64'>      coord           /         lat
lon                                                  [2, 3]  numpy.ndarray[tuple[typing.Any, ...], numpy.dt...   {'long_name': 'Longitude', 'units': 'deg'}      (lon,)  <class 'numpy.float64'>      coord           /         lon
location                                              Tokyo                                      <class 'str'>                                         None        None                     None       attr           /    location
```
