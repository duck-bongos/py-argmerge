import json
import os
import sys
from pathlib import Path
from typing import Any

from loguru import logger as LOGGER

cpdef tuple[dict, dict] parse_json(threshold_kwargs: dict[str, Any], change_ledger: dict[str, dict[str, str | int]], fpath_json: str | Path, debug: bool = False):

    cdef dict _json_kwargs
    cdef str _cli_input
    cdef list[tuple[str, str]] cli_matches

    if debug:
        LOGGER.remove()
        LOGGER.add(sys.stderr, level="DEBUG")

    LOGGER.debug(f"{threshold_kwargs=}")
    LOGGER.debug(f"{fpath_json=}")

    _fpath_json = Path(fpath_json)
    if _fpath_json.suffix != ".json":
        raise ValueError(
            f"The JSON suffix of {_fpath_json.as_posix()} is not correct."
            " Please use '.json'."
        )

    with open(fpath_json, 'rb') as fy:
        _json_kwargs = json.load(fy)

    LOGGER.debug(f"{_json_kwargs=}")
    threshold_kwargs.update(_json_kwargs)
    LOGGER.debug(f"Updated {threshold_kwargs=}")

    for key in _json_kwargs:
        change_ledger[key] = {"label": f"JSON ({_fpath_json})", "rank": 10}

    return threshold_kwargs, change_ledger

    