import os
import sys
from pathlib import Path

import yaml
from loguru import logger as LOGGER

cpdef tuple[dict, dict] parse_yaml(threshold_kwargs: dict[str, str], change_ledger: dict[str, dict[str, str | int]], fpath_yaml: str | Path, debug: bool = False):

    cdef dict _yaml_kwargs
    cdef str _cli_input
    cdef list[tuple[str, str]] cli_matches

    if debug:
        LOGGER.remove()
        LOGGER.add(sys.stderr, level="DEBUG")

    LOGGER.debug(f"{threshold_kwargs=}")
    LOGGER.debug(f"{fpath_yaml=}")

    _fpath_yaml = Path(fpath_yaml)
    if _fpath_yaml.suffix not in (".yml", ".yaml"):
        raise ValueError(
            f"The YAML suffix of '{_fpath_yaml.suffix}' is not correct."
            " Please use '.yml' or '.yaml'."
        )

    with open(fpath_yaml, 'rb') as fy:
        _yaml_kwargs = yaml.safe_load(fy)

    LOGGER.debug(f"{_yaml_kwargs=}")
    threshold_kwargs.update(_yaml_kwargs)
    LOGGER.debug(f"Updated {threshold_kwargs=}")

    for key in _yaml_kwargs:
        change_ledger[key] = {"label": f"YAML ({_fpath_yaml})", "rank": 20}

    return threshold_kwargs, change_ledger

    