import os
import sys
from inspect import signature, Parameter
from typing import Any, Callable
from loguru import logger as LOGGER

cpdef dict parse_func(f: Callable, debug: bool = False):
    cdef dict _default

    if debug:
        LOGGER.remove()
        LOGGER.add(sys.stderr, level="DEBUG")
        
    _sig = signature(f)
    LOGGER.debug(f"Function {signature=}")

    _default = {}

    for k, v in _sig.parameters.items():
        if v.default is not Parameter.empty:
            _default[k] = v

    LOGGER.debug(f"{_default=}")
    return _default

cpdef tuple[dict, dict] update_from_function(threshold_kwargs: dict[str, Any], change_ledger: dict[str, dict[str, str | int]], func_kwargs: dict[str, Any], debug: bool = False):
    if debug:
        LOGGER.remove()
        LOGGER.add(sys.stderr, level="DEBUG")

    LOGGER.debug(f"{threshold_kwargs=}")
    LOGGER.debug(f"{func_kwargs=}")

    _threshold_kwargs = threshold_kwargs.copy()

    threshold_kwargs.update(**func_kwargs)

    for key in func_kwargs:
        change_ledger[key] = {"label": "developer-provided", "rank": 100}

    return threshold_kwargs, change_ledger