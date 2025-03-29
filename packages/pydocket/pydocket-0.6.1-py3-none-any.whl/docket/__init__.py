"""
docket - A distributed background task system for Python functions.

docket focuses on scheduling future work as seamlessly and efficiently as immediate work.
"""

from importlib.metadata import version

__version__ = version("pydocket")

from .annotations import Logged
from .dependencies import (
    CurrentDocket,
    CurrentExecution,
    CurrentWorker,
    Depends,
    ExponentialRetry,
    Perpetual,
    Retry,
    TaskKey,
    TaskLogger,
    Timeout,
)
from .docket import Docket
from .execution import Execution
from .worker import Worker

__all__ = [
    "Docket",
    "Worker",
    "Execution",
    "CurrentDocket",
    "CurrentWorker",
    "CurrentExecution",
    "TaskKey",
    "TaskLogger",
    "Retry",
    "ExponentialRetry",
    "Logged",
    "Perpetual",
    "Timeout",
    "Depends",
    "__version__",
]
