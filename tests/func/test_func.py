"""Unit tests for the argmerge._func::{parse_func, update_from_function} functions."""

import pytest
from argmerge._func import parse_func, update_from_function

from tests.utils import no_error


# [parse_func]
def no_default_params(a: int, b: str, c: float):
    pass


def mixed_params(a: int, b: str, c: float = 0.0):
    pass


def all_default_params(a: int = 7, b: str = "", c: float = 0.0):
    pass


@pytest.mark.parametrize(
    "function, debug,expected_kwargs, expected_ledger, context",
    [
        # if not a callable is passed
        (None, False, None, None, pytest.raises(TypeError)),
        # if no parameters with defaults are passed
        (no_default_params, False, {}, {}, no_error),
        # if mix of default/not default params are passed
        (
            mixed_params,
            True,
            {"c": 0.0},
            {"c": {"label": "Python Function default", "rank": 0}},
            no_error,
        ),
        # if all functions have defaults
        (
            all_default_params,
            True,
            {"a": 7, "b": "", "c": 0.0},
            {
                "c": {"label": "Python Function default", "rank": 0},
                "b": {"label": "Python Function default", "rank": 0},
                "a": {"label": "Python Function default", "rank": 0},
            },
            no_error,
        ),
    ],
)
def test_parse_func(function, debug, expected_kwargs, expected_ledger, context):
    with context:
        _expected_kwargs, _expected_ledger = parse_func(function, debug)
        assert expected_kwargs == _expected_kwargs
        assert expected_ledger == _expected_ledger


# [update_from_function]
@pytest.mark.parametrize(
    "threshold_kwargs,change_ledger,func_kwargs,debug,expected_kwargs,expected_ledger,context,",
    [
        # no previous changes
        (
            {},
            {},
            {"a": 1},
            False,
            {"a": 1},
            {"a": {"label": "developer-provided", "rank": 100}},
            no_error,
        ),
        # one previous change
        (
            {"a": 3},
            {"a": {"label": "Python Function default", "rank": 0}},
            {"a": 1},
            False,
            {"a": 1},
            {"a": {"label": "developer-provided", "rank": 100}},
            no_error,
        ),
        # many previous changes from many levels
        (
            {"a": 1, "b": "", "c": 0.0},
            {
                "a": {"label": "Python Function default", "rank": 0},
                "b": {"label": "Environment Variable", "rank": 30},
                "c": {"label": "CLI", "rank": 40},
            },
            {"a": 99, "b": "Ken Thompson", "c": -0.8},
            False,
            {"a": 99, "b": "Ken Thompson", "c": -0.8},
            {
                "a": {"label": "developer-provided", "rank": 100},
                "b": {"label": "developer-provided", "rank": 100},
                "c": {"label": "developer-provided", "rank": 100},
            },
            no_error,
        ),
    ],
)
def test_update_from_function(
    threshold_kwargs,
    change_ledger,
    func_kwargs,
    debug,
    expected_kwargs,
    expected_ledger,
    context,
):
    with context:
        _expected_kwargs, _expected_ledger = update_from_function(
            threshold_kwargs, change_ledger, func_kwargs, debug
        )
        assert expected_kwargs == _expected_kwargs
        assert expected_ledger == _expected_ledger
