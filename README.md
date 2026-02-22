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
from xarrayspecs import asarray, asset, astree, attrs, dims, dtype, use


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
asarray(weather)
```
```
<xarray.DataArray 'temp' (lon: 2, lat: 2)> Size: 32B
array([[280.83091127, 273.43442136],
       [287.12430824, 276.21645775]])
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
asset(weather)
```
```
<xarray.Dataset> Size: 96B
Dimensions:  (lat: 2, lon: 2)
Coordinates:
  * lat      (lat) float64 16B 0.0 1.0
  * lon      (lon) float64 16B 2.0 3.0
Data variables:
    temp     (lon, lat) float64 32B 285.6 279.2 274.6 291.4
    wind     (lon, lat) float64 32B 6.964 2.388 4.241 1.262
```

### Create a DataTree from the specification

```python
astree(weather)
```
```
<xarray.DataTree>
Group: /
    Dimensions:  (lat: 2, lon: 2)
    Coordinates:
      * lat      (lat) float64 16B 0.0 1.0
      * lon      (lon) float64 16B 2.0 3.0
    Data variables:
        temp     (lon, lat) float64 32B 285.6 279.2 274.6 291.4
        wind     (lon, lat) float64 32B 6.964 2.388 4.241 1.262
```
