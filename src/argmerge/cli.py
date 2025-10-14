"""Module that provides a flexible CLI parser component in the decorator."""

import re
import sys
from typing import Any

from loguru import logger as LOGGER

from argmerge.base import SourceParser

__all__ = ["CLI_PATTERN", "parse_cli"]

# matches '--arg=value'
# does not match '--arg value'
CLI_PATTERN: re.Pattern = re.compile(r"--([A-Za-z\_\-]+)\=([0-9A-Za-z\_\-\.]+)")


class CLIParser(SourceParser):
    """The parser the extracts relevant CLI arguments.

    Vars:
        label (str):

    """

    label: str = "CLI"
    rank: int = 40

    def __call__(
        cls,
        threshold_kwargs: dict[str, Any],
        change_ledger: dict[str, dict[str, str | int]],
        cli_pattern: re.Pattern[str] = CLI_PATTERN,
        debug: bool = False,
        **kwargs,
    ) -> tuple[dict, dict]:
        _cli_kwargs: dict
        _cli_input: str

        if debug:
            LOGGER.remove()
            LOGGER.add(sys.stderr, level="DEBUG")

        if isinstance(cli_pattern, re.Pattern):
            _cli_pattern = cli_pattern

        else:
            _cli_pattern = re.compile(rf"{cli_pattern}")

        LOGGER.debug(f"{cli_pattern=}")
        LOGGER.debug(f"{_cli_pattern=}")
        LOGGER.debug(f"{sys.argv=}")
        _cli_input = " ".join(sys.argv[1:])
        LOGGER.debug(f"{_cli_input}")

        _cli_kwargs = dict(_cli_pattern.findall(_cli_input))
        LOGGER.debug(f"{_cli_kwargs=}")

        threshold_kwargs.update(_cli_kwargs)
        LOGGER.debug(f"Updated {threshold_kwargs=}")

        for key in _cli_kwargs:
            change_ledger[key] = {"label": cls.label, "rank": cls.rank}

        return threshold_kwargs, change_ledger


parse_cli = CLIParser()
