import functools
import re
from pathlib import Path

from argmerge.cli import CLI_PATTERN, parse_cli
from argmerge.env import ENV_PREFIX, parse_env
from argmerge.func import parse_func, update_from_function
from argmerge.json import parse_json
from argmerge.trace import LOG_LEVELS, trace_arg_lineage
from argmerge.yaml import parse_yaml


def threshold(
    *args,
    fpath_json: str | Path = "",
    fpath_yaml: str | Path = "",
    env_prefix: str | re.Pattern[str] = ENV_PREFIX,  # 'THRESH', also set at PYTHRESH
    cli_pattern: str | re.Pattern[str] = CLI_PATTERN,
    trace_level: str = "",
    debug: bool = False,
    **kwargs,
):
    if len(args) == 1:
        # allow syntax of @threshold and @threshold()
        return threshold()(args[0])

    else:

        def wrapped(f):
            @functools.wraps(f)
            def wrapped_f(*_args, **_kwargs):
                _threshold_kwargs, _change_ledger = dict(), dict()
                _threshold_kwargs, _change_ledger = parse_func(
                    _threshold_kwargs, _change_ledger, f, debug=debug
                )

                _threshold_kwargs, _change_ledger = parse_json(
                    _threshold_kwargs,
                    _change_ledger,
                    fpath_json=fpath_json,
                    debug=debug,
                )

                _threshold_kwargs, _change_ledger = parse_yaml(
                    _threshold_kwargs,
                    _change_ledger,
                    fpath_yaml=fpath_yaml,
                    debug=debug,
                )

                _threshold_kwargs, _change_ledger = parse_env(
                    _threshold_kwargs,
                    _change_ledger,
                    env_prefix=env_prefix,
                    debug=debug,
                )

                _threshold_kwargs, _change_ledger = parse_cli(
                    _threshold_kwargs,
                    _change_ledger,
                    cli_pattern=cli_pattern,
                    debug=debug,
                )

                _threshold_kwargs, _change_ledger = update_from_function(
                    _threshold_kwargs, _change_ledger, func_kwargs=_kwargs, debug=debug
                )

                if trace_level.lower() in LOG_LEVELS:
                    trace_arg_lineage(
                        f,
                        _change_ledger,
                        level=trace_level,
                    )

                elif trace_level == "":
                    # default behavior
                    pass

                else:
                    raise ValueError(
                        f"'trace_level' has been set to '{trace_level}', which is not "
                        "supported. Please set 'trace_level' to an empty string or one"
                        f" of: {LOG_LEVELS}."
                    )

                return f(*_args, **_threshold_kwargs)

            return wrapped_f

        return wrapped
