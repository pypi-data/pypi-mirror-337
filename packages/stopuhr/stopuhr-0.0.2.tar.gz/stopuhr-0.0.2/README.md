# stopuhr

A simple tool for measuring durations in Python.

## Installation

You can install stopuhr via pip:

```sh
pip install stopuhr
```

However, `uv` is recommended for installing python packages:

```sh
uv add stopuhr
```

## Usage

With stopuhr it is convinient to measure durations in Python:

```python
from stopuhr import stopuhr

with stopuhr("My Timer"):
    # Do something
    pass
```

For a stateful version, a decorator or a stateful decorator please visit the Reference or have a look at the examples.
