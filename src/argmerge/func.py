"""Module to work with functions"""

# cython: linetrace=True
import sys
from inspect import Parameter, signature
from typing import Any, Callable

from loguru import logger as LOGGER

from argmerge.base import SourceParser

__all__ = ["parse_func", "parse_func_runtime"]


class FuncParser(SourceParser):
    label: str = "Python Function default"
    rank: int = 0

    def __call__(
        cls,
        threshold_kwargs: dict,
        change_ledger: dict,
        f: Callable,
        debug: bool = False,
    ) -> tuple[dict, dict]:
        """Lowest level parser - retrieve function defaults as fallback arguments.

        Args:
            f (callable):
            debug (bool):

        """
        _default: dict

        if debug:
            LOGGER.remove()
            LOGGER.add(sys.stderr, level="DEBUG")

        _sig = signature(f)
        LOGGER.debug(f"Function {signature=}")

        _default = {}

        for k, v in _sig.parameters.items():
            if v.default is not Parameter.empty:
                _default[k] = v.default

        LOGGER.debug(f"{_default=}")
        _change_ledger = {k: {"label": cls.label, "rank": 0} for k in _default.copy()}
        return _default, _change_ledger


parse_func = FuncParser()


class FuncUpdater(SourceParser):
    label: str = "developer-provided"
    rank: int = 100

    def __call__(
        cls,
        threshold_kwargs: dict[str, Any],
        change_ledger: dict[str, dict[str, str | int]],
        func_kwargs: dict[str, Any],
        debug: bool = False,
    ) -> tuple[dict, dict]:
        if debug:
            LOGGER.remove()
            LOGGER.add(sys.stderr, level="DEBUG")

        LOGGER.debug(f"{threshold_kwargs=}")
        LOGGER.debug(f"{func_kwargs=}")

        threshold_kwargs.update(**func_kwargs)

        for key in func_kwargs:
            change_ledger[key] = {"label": cls.label, "rank": cls.rank}

        return threshold_kwargs, change_ledger


parse_func_runtime = FuncUpdater()
