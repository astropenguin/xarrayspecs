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
from dataclasses import dataclass
from numpy.typing import NDArray
from typing import Annotated, Any
from xarrayspecs import attrs, dims, dtype, use


@dataclass
class Weather:
    temp: Annotated[
        NDArray[Any],
        use("data"),
        dims(["lon", "lat"]),
        dtype(np.float64),
        attrs({"long_name": "Temperature", "units": "K"}),
    ]
    wind: Annotated[
        NDArray[Any],
        use("data"),
        dims(["lon", "lat"]),
        dtype(np.float64),
        attrs({"long_name": "Wind speed", "units": "m/s"}),
    ]
    lat: Annotated[
        NDArray[Any],
        use("coord"),
        dims("lat"),
        dtype(np.float64),
        attrs({"long_name": "Latitude", "units": "deg"}),
    ]
    lon: Annotated[
        NDArray[Any],
        use("coord"),
        dims("lon"),
        dtype(np.float64),
        attrs({"long_name": "Longitude", "units": "deg"}),
    ]
    location: Annotated[str, use("attr")] = "Tokyo"


weather = Weather(
    np.random.uniform(273, 293, size=(2, 2)),
    np.random.uniform(0, 10, size=(2, 2)),
    np.array([0, 1]),
    np.array([2, 3]),
)
```

### Create a DataArray from the specification

```python
from xarrayspecs import asarray


print(asarray(weather))
```
```
<xarray.DataArray 'temp' (lon: 2, lat: 2)> Size: 32B
array([[281.91025577, 273.71846374],
       [292.65314453, 288.82971128]])
Coordinates:
  * lon      (lon) float64 16B 2.0 3.0
  * lat      (lat) float64 16B 0.0 1.0
Attributes:
    long_name:  Temperature
    units:      K
    location:   Tokyo
```

### Create a Dataset from the specification

```python
from xarrayspecs import asset


print(asset(weather))
```
```
<xarray.Dataset> Size: 96B
Dimensions:  (lat: 2, lon: 2)
Coordinates:
  * lat      (lat) float64 16B 0.0 1.0
  * lon      (lon) float64 16B 2.0 3.0
Data variables:
    temp     (lon, lat) float64 32B 281.9 273.7 292.7 288.8
    wind     (lon, lat) float64 32B 4.61 7.003 8.294 9.636
Attributes:
    location:  Tokyo
```

### Create a DataTree from the specification

```python
from xarrayspecs import astree


print(astree(weather))
```
```
<xarray.DataTree>
Group: /
    Dimensions:  (lat: 2, lon: 2)
    Coordinates:
      * lat      (lat) float64 16B 0.0 1.0
      * lon      (lon) float64 16B 2.0 3.0
    Data variables:
        temp     (lon, lat) float64 32B 281.9 273.7 292.7 288.8
        wind     (lon, lat) float64 32B 4.61 7.003 8.294 9.636
    Attributes:
        location:  Tokyo
```

## Advanced Usage

### Check the parsed specification

```python
from xarrayspecs import parse


print(parse(weather))
```
```
                                                       data  \
temp      [[281.91025577121246, 273.71846373599766], [29...
wind      [[4.609535345832531, 7.002675235912125], [8.29...
lat                                                  [0, 1]
lon                                                  [2, 3]
location                                              Tokyo

                                                       type  \
temp      numpy.ndarray[tuple[typing.Any, ...], numpy.dt...
wind      numpy.ndarray[tuple[typing.Any, ...], numpy.dt...
lat       numpy.ndarray[tuple[typing.Any, ...], numpy.dt...
lon       numpy.ndarray[tuple[typing.Any, ...], numpy.dt...
location                                      <class 'str'>

                                         xarray_attrs xarray_dims  \
temp       {'long_name': 'Temperature', 'units': 'K'}  (lon, lat)
wind      {'long_name': 'Wind speed', 'units': 'm/s'}  (lon, lat)
lat         {'long_name': 'Latitude', 'units': 'deg'}      (lat,)
lon        {'long_name': 'Longitude', 'units': 'deg'}      (lon,)
location                                         None        None

                     xarray_dtype xarray_use xarray_node xarray_name
temp      <class 'numpy.float64'>       data           /        temp
wind      <class 'numpy.float64'>       data           /        wind
lat       <class 'numpy.float64'>      coord           /         lat
lon       <class 'numpy.float64'>      coord           /         lon
location                     None       attr           /    location
```
