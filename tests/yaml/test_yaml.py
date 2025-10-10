"""Unit tests for the argmerge._yaml::parse_yaml() function."""

import pytest
from argmerge._yaml import parse_yaml
from yaml.scanner import ScannerError

from tests.utils import no_error

fpath_bad = "fpath_config.json"


@pytest.mark.parametrize(
    "threshold_kwargs,change_ledger,fpath_yaml,debug,expected_kwargs,expected_ledger,context",
    [
        # file does not exist
        pytest.param(
            {},
            {},
            "missing_config.yaml",
            False,
            None,
            None,
            pytest.raises(FileNotFoundError),
        ),
        # wrong filepath extension -> ValueError
        pytest.param(
            {},
            {},
            fpath_bad,
            False,
            None,
            None,
            pytest.raises(ValueError),
        ),
        # broken YAML -> error
        pytest.param(
            {},
            {},
            "tests/yaml/bad_config.yaml",
            False,
            None,
            None,
            pytest.raises(ScannerError),
        ),
        # working example
        # debug true
        pytest.param(
            {},
            {},
            "tests/yaml/good_config.yaml",
            True,
            {"a": 1, "b": {"c": 3, "d": 4}},
            {
                "a": {"label": "YAML (tests/yaml/good_config.yaml)", "rank": 20},
                "b": {"label": "YAML (tests/yaml/good_config.yaml)", "rank": 20},
            },
            no_error,
        ),
        # debug false
        pytest.param(
            {"a": 7, "c": 9},
            {
                "a": {"label": "JSON (other.json)", "rank": 10},
                "c": {"label": "JSON (other.json)", "rank": 10},
            },
            "tests/yaml/good_config.yaml",
            True,
            {"a": 1, "b": {"c": 3, "d": 4}, "c": 9},
            {
                "a": {"label": "YAML (tests/yaml/good_config.yaml)", "rank": 20},
                "b": {"label": "YAML (tests/yaml/good_config.yaml)", "rank": 20},
                "c": {"label": "JSON (other.json)", "rank": 10},
            },
            no_error,
        ),
    ],
)
def test_parse_yaml(
    threshold_kwargs,
    change_ledger,
    fpath_yaml,
    debug,
    expected_kwargs,  # output[0]
    expected_ledger,  # output[1]
    context,  # whether or not is an error
):
    with context:
        threshold_kwargs_, change_ledger_ = parse_yaml(
            threshold_kwargs, change_ledger, fpath_yaml, debug=debug
        )
        assert threshold_kwargs_ == expected_kwargs
        assert change_ledger_ == expected_ledger
