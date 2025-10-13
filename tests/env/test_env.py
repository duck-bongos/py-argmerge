"""Unit tests for the argmerge._func::{parse_func, update_from_function} functions."""

import re

import pytest

from argmerge.env import ENV_PREFIX, parse_env
from tests.utils import no_error

# string pattern
# regex pattern
# neither string/regex pattern


@pytest.mark.parametrize(
    "env_mapping,threshold_kwargs,change_ledger,env_prefix,debug,expected_kwargs,"
    "expected_ledger,context,",
    [
        # No Environment Variables - no change
        (
            {},
            {"a": 1},
            {"a": {"label": "Python Function default", "rank": 0}},
            "THRESH",
            False,
            {"a": 1},
            {"a": {"label": "Python Function default", "rank": 0}},
            no_error,
        ),
        # No relevant Environment Variables
        (
            {"COLORTERM": "truecolor"},
            {"a": 1},
            {"a": {"label": "Python Function default", "rank": 0}},
            "THRESH",
            False,
            {"a": 1},
            {"a": {"label": "Python Function default", "rank": 0}},
            no_error,
        ),
        # Two Environment Variables - extractable values
        (
            {"THRESH_A": "99", "THRESH_B": "2"},
            {"a": 1},
            {"a": {"label": "Python Function default", "rank": 0}},
            "THRESH",
            True,
            {"a": 99, "b": 2},
            {
                "a": {"label": "Environment Variable", "rank": 30},
                "b": {"label": "Environment Variable", "rank": 30},
            },
            no_error,
        ),
        # Three environment variables, one is a string
        (
            {"THRESH_A": "99", "THRESH_B": "2", "THRESH_C": "laugh"},
            {"a": 1},
            {"a": {"label": "Python Function default", "rank": 0}},
            "THRESH",
            True,
            {"a": 99, "b": 2, "c": "laugh"},
            {
                "a": {"label": "Environment Variable", "rank": 30},
                "b": {"label": "Environment Variable", "rank": 30},
                "c": {"label": "Environment Variable", "rank": 30},
            },
            no_error,
        ),
        # Use the environment variable to retrieve the prefix, PYTHRESH
        (
            {"NOT_RELEVANT_A": "99", "THRESH_B": "2.0", "THRESH_C": "laugh"},
            {"a": 1},
            {"a": {"label": "Python Function default", "rank": 0}},
            ENV_PREFIX,
            True,
            {"a": 1, "b": 2.0, "c": "laugh"},
            {
                "a": {"label": "Python Function default", "rank": 0},
                "b": {"label": "Environment Variable", "rank": 30},
                "c": {"label": "Environment Variable", "rank": 30},
            },
            no_error,
        ),
        # Do NOT Provide a capture group in the regex pattern
        # this will skip THRESH_B an THRESH_C
        # The proper Regex is r'^THRESH.([A-Z_-]+)$'
        (
            {"NOT_RELEVANT_A": "99", "THRESH_B": "2.0", "THRESH_C": "laugh"},
            {"a": 1},
            {"a": {"label": "Python Function default", "rank": 0}},
            re.compile("^THRESH.[A-Z_-]+"),
            True,
            {"a": 1},
            {
                "a": {"label": "Python Function default", "rank": 0},
            },
            no_error,
        ),
        (
            {"NOT_RELEVANT_A": "99", "THRESH_B": "2.0", "THRESH_C": "laugh"},
            {"a": 1},
            {"a": {"label": "Python Function default", "rank": 0}},
            77,
            True,
            {"a": 1, "b": 2.0, "c": "laugh"},
            {
                "a": {"label": "Python Function default", "rank": 0},
                "b": {"label": "Environment Variable", "rank": 30},
                "c": {"label": "Environment Variable", "rank": 30},
            },
            pytest.raises(ValueError),
        ),
    ],
)
def test_parse_env(
    monkeypatch,
    env_mapping,
    threshold_kwargs,
    change_ledger,
    env_prefix,
    debug,
    expected_kwargs,
    expected_ledger,
    context,
):
    with monkeypatch.context() as m:
        for env_var_name, env_var_value in env_mapping.items():
            m.setenv(env_var_name, env_var_value)

        with context:
            threshold_kwargs_, change_ledger_ = parse_env(
                threshold_kwargs, change_ledger, env_prefix, debug
            )
            assert threshold_kwargs_ == expected_kwargs
            assert change_ledger_ == expected_ledger
