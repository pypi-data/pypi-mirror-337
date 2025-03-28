"""Very high level benchmarking decorator."""

import logging
from typing import TYPE_CHECKING

from stopuhr.stopuhr import StopUhr, stopuhr

if TYPE_CHECKING:
    import pandas as pd


class FunkUhr:
    """Very high level benchmarking decorator.

    Wraps the `StopUhr` class to provide a decorator for benchmarking functions.

    Example:
        A stateful decorator exists as well, which is just a wrapper around the stateful timer.
        It supports the same arguments as the stateful timer.

        .. code-block:: python

            >>> from stopuhr import FunkUhr

            >>> funkuhr = FunkUhr()

            >>> @funkuhr("Busy Function", log=False)
            >>> def busy_function():
            >>>     time.sleep(0.1)

            >>> for i in range(5):
            >>>     busy_function()

            >>> funkuhr.summary()
            Busy Function took 0.10 ± 0.00 s (n=5 -> total=0.50s)

    """

    def __init__(self, logger: logging.Logger | None = None):
        """FunkUhr: a very high level benchmarking decorator.

        Args:
            logger (logging.Logger | None, optional): A logger to print the output to instead of stdout.
                Defaults to None.

        """
        self.stopuhr = StopUhr(logger)

    def export(self) -> "pd.DataFrame":
        """Export the durations as a pandas DataFrame.

        Returns:
            pd.DataFrame: A pandas DataFrame with the durations.

        """
        return self.stopuhr.export()

    def summary(self, res: int = 2):
        """Print a summary of the durations.

        Args:
            res (int, optional): The number of decimal places to round to. Defaults to 2.

        """
        self.stopuhr.summary(res)

    def __call__(self, key: str, res: int = 2, log: bool = True):
        """Decorate a function to measure the time taken in a block.

        Args:
            key (str): The key to store the duration under.
            res (int, optional): The number of decimal places to round to. Defaults to 2.
            log (bool, optional): Whether to log the duration. Defaults to True.

        """

        def _decorator(func):
            def _inner(*args, **kwargs):
                with self.stopuhr(key, res=res, log=log):
                    return func(*args, **kwargs)

            return _inner

        return _decorator


def funkuhr(msg: str, printer: callable = print, res: int = 2):
    """Decorate a function to measure the time taken in a block.

    Wraps the `stopuhr` function to provide a decorator for benchmarking functions.

    Example:
        .. code-block:: python

            >>> from stopuhr import funkuhr

            >>> @funkuhr("Busy Function")
            >>> def busy_function():
            >>>     time.sleep(0.2)

            >>> busy_function()
            Busy Function took 0.20s

    Args:
        func (callable): The function to decorate.
        msg (str): The message to print.
        printer (callable, optional): The function to print with. Defaults to print.
        res (int, optional): The number of decimal places to round to. Defaults to 2.

    """

    def _decorator(func):
        def _inner(*args, **kwargs):
            with stopuhr(msg, printer, res):
                return func(*args, **kwargs)

        return _inner

    return _decorator


__all__ = ["FunkUhr", "funkuhr"]
