import json
import sys
from pathlib import Path
from typing import Any

from loguru import logger as LOGGER

from argmerge.base import SourceParser

__all__ = ["parse_json"]


class JSONParser(SourceParser):
    label: str = "JSON"
    rank: int = 10

    def __call__(
        cls,
        threshold_kwargs: dict[str, Any],
        change_ledger: dict[str, dict[str, str | int]],
        fpath_json: str | Path,
        debug: bool = False,
    ) -> tuple[dict, dict]:
        _json_kwargs: dict

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

        cls.label = f"JSON ({_fpath_json})"

        with open(fpath_json, "rb") as fy:
            _json_kwargs = json.load(fy)

        LOGGER.debug(f"{_json_kwargs=}")
        threshold_kwargs.update(_json_kwargs)
        LOGGER.debug(f"Updated {threshold_kwargs=}")

        for key in _json_kwargs:
            change_ledger[key] = {"label": cls.label, "rank": cls.rank}

        return threshold_kwargs, change_ledger


parse_json = JSONParser()
