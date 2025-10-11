"""Unit tests for the argmerge._func::{parse_func, update_from_function} functions."""

import pytest
from argmerge._func import parse_func

# [parse_func]


@pytest.mark.parametrize(
    "function, debug,expected_kwargs, expected_ledger, context",
    [
        # if not a callable is passed
        (None, False, None, None, pytest.raises(TypeError)),
        # if no parameters with defaults are passed
        # if mix of default/not default params are passed
        # ()
        # if all functions have defaults
        # ()
    ],
)
def test_parse_func(function, debug, expected_kwargs, expected_ledger, context):
    with context:
        _expected_kwargs, _expected_ledger = parse_func(function, debug)
        assert expected_kwargs == _expected_kwargs
        assert expected_ledger == _expected_ledger


# if not a callable is passed
# if no parameters with defaults are passed
# if mix of default/not default params are passed
# if all functions have defaults

# [update_from_function]
