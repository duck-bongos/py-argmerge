# cython: linetrace=True
# distutils: define_macros=CYTHON_TRACE=1

import sys
from inspect import signature
from typing import Callable

from loguru import logger as LOGGER

LOG_LEVELS = ("critical", "warning", "success", "info", "debug")


def _write_trace(message: str, level: str):
    if isinstance(level, str):
        _level = level.lower()

    else:
        raise TypeError(f"Log level '{level}' ({type(level)}) is not a string.")

    if _level not in LOG_LEVELS:
        raise ValueError(
            f"Log level '{_level}' not in basic loguru log levels: '{LOG_LEVELS}''."
        )

    _trace_logger: int = LOGGER.add(sys.stderr, level=level.upper())

    getattr(LOGGER, _level.lower())(message)

    LOGGER.remove(_trace_logger)


def _log_trace(ledger: dict[str, dict[str, str | int]], level: str = ""):
    if len(ledger) == 0:
        LOGGER.warning("Change ledger is empty, will not write out!")

    else:
        ranks = {k: v["rank"] for k, v in ledger.items()}
        labels = {k: v["label"] for k, v in ledger.items()}
        sorted_keys = [x for x, _ in sorted(ranks.items(), key=lambda x: x[1])]
        sorted_labels = {k: labels[k] for k in sorted_keys}

        _key_spacing = max(list(map(len, sorted_labels.keys())))
        _value_spacing = max(list(map(len, sorted_labels.values())))
        _pre_join_spacing = {
            k.ljust(_key_spacing, " "): v.ljust(_value_spacing, " ")
            for k, v in sorted_labels.items()
        }
        _params = [f"{k}\t| {v}" for k, v in _pre_join_spacing.items()]
        _heading_spacing = max(map(len, _params)) + 7
        _heading_param = "Parameter Name".ljust(_key_spacing)
        _heading_loc = "Location Set".ljust(_value_spacing)
        _heading = f"{_heading_param}\t| {_heading_loc}"
        _join = "\n".join(_params)
        msg = f"\n{_heading}\n{'=' * _heading_spacing}\n{_join}"

        _write_trace(message=msg, level=level)


def trace_arg_lineage(
    f: Callable,
    change_ledger: dict[str, str],
    level: str = "",
):
    sig = signature(f)
    _changed = {k: v for k, v in change_ledger.items() if k in sig.parameters}

    _log_trace(ledger=_changed, level=level)
