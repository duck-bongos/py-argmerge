import os
import sys
import re
from typing import Any

from loguru import logger as LOGGER

from argmerge._utils import extract_literals

ENV_PREFIX = os.environ.get("PYTHRESH", "THRESH")


cpdef tuple[dict, dict] parse_env(threshold_kwargs: dict[str, Any], change_ledger: dict[str, dict[str, str | int]], env_prefix: str | re.Pattern[str] = ENV_PREFIX, debug: bool = False):
    cdef dict _env_kwargs
    cdef str _env_prefix = env_prefix.upper()

    if debug:
        LOGGER.remove()
        LOGGER.add(sys.stderr, level="DEBUG")

    if isinstance(env_prefix, re.Pattern):
        pattern = env_prefix

    elif isinstance(env_prefix, str):
        pattern = re.compile(rf"(?:{env_prefix}.)([A-Za-z0\-\_]+)")
    
    else:
        raise ValueError(f"'env_prefix' must be either a string or Regex string pattern. Received: {env_prefix} ({type(env_prefix)}).")

    LOGGER.debug(f"{env_prefix=}")
    LOGGER.debug(f"{pattern=}")
    
    _env_kwargs = {}

    for k, v in os.environ.items():
        _search = pattern.search(k)

        if _search is not None:
            key = _search.group(1).lower()
            LOGGER.debug(f"{key=} {v=}")
            _env_kwargs[key] = extract_literals(v)

        else:
            LOGGER.debug(f"Miss: {k=}")

    LOGGER.debug(f"{_env_kwargs=}")
    threshold_kwargs.update(_env_kwargs)
    
    LOGGER.debug(f"Updated {threshold_kwargs=}")

    for key in _env_kwargs:
        change_ledger[key] = {"label": "Environment Variable", "rank": 30}

    return threshold_kwargs, change_ledger