# ruff: noqa: D205, D212, D400, D415, E402, D103
"""
===================
Basic Usage Example
===================

This is a basic usage example of the `stopuhr` package.

"""

# %%
# Stop the time with a simple context manager and print the duration.
import time

from stopuhr import stopuhr

with stopuhr("Sleeping"):
    time.sleep(0.1)

# %%
# Instead of printing, one can pass any callable to the `printer` argument, e.g. a logger.
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

with stopuhr("Sleeping", printer=logger.info):
    time.sleep(0.1)

# %%
# By default, the output is rounded to two decimal places. This can be changed with the `res` argument.
with stopuhr("Sleeping", res=3):
    time.sleep(0.16189)


# %%
# Use a stateful timer to measure the time taken in a loop.
# This also supports the `printer` and `res` arguments.
# The `log` argument of each call can be used to suppress the output.
from stopuhr import StopUhr

stopuhr = StopUhr()

for i in range(5):
    with stopuhr("Sleeping", log=False):
        time.sleep(0.2)

# Print a summary with the mean and standard deviation of the durations.
stopuhr.summary()

# %%
# The `reset`` command resets the state of the timer, note that this function is happening in-place.
stopuhr.reset()

# %%
# The previous behavior can be achieved with the `start` and `stop` methods.
# Here, the `stop` method also supports the `log` and `res` arguments.
for i in range(5):
    stopuhr.start("Sleeping")
    time.sleep(0.2)
    stopuhr.stop("Sleeping", log=False)

stopuhr.summary()

# %%
# The stateful timer can also measure multiple durations at once.

stopuhr.reset()

# Single duration
with stopuhr("A (single 0.2s sleep)", log=False):
    time.sleep(0.2)

for i in range(5):
    with stopuhr("B (multiple 0.2s sleeps)", log=False):
        time.sleep(0.2)
    with stopuhr("C (multiple 0.1s sleeps)", log=False):
        time.sleep(0.1)

stopuhr.summary()

# %%
# A stateless decorator can be used to measure the duration of a function.
# The decorator expects a message / key, just like the others and also supports the `printer` and `res` arguments.
from stopuhr import funkuhr


@funkuhr("Busy Function")
def busy_function():
    time.sleep(0.2)


busy_function()

# %%
# A stateful decorator exists as well, which is just a wrapper around the stateful timer.
# It supports the same arguments as the stateful timer.
from stopuhr import FunkUhr

funkuhr = FunkUhr()


@funkuhr("Busy Function", log=False)
def busy_function():
    time.sleep(0.1)


for i in range(5):
    busy_function()

funkuhr.summary()
