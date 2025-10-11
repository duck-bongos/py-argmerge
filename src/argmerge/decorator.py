import functools
import re
from pathlib import Path
from warnings import warn

from argmerge._cli import CLI_PATTERN, parse_cli
from argmerge._env import ENV_PREFIX, parse_env
from argmerge._func import parse_func, update_from_function
from argmerge._json import parse_json
from argmerge._trace import LOG_LEVELS, trace_arg_lineage
from argmerge._yaml import parse_yaml


def threshold(
    *args,
    fpath_json: str | Path = "",
    fpath_yaml: str | Path = "",
    env_prefix: str | re.Pattern[str] = ENV_PREFIX,  # 'THRESH', also set at PYTHRESH
    cli_pattern: str | re.Pattern[str] = CLI_PATTERN,
    trace_args: str = "",
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
                _threshold_kwargs, _change_ledger = parse_func(f, debug=debug)

                if Path(fpath_json).suffix == ".json":
                    _threshold_kwargs, _change_ledger = parse_json(
                        _threshold_kwargs,
                        _change_ledger,
                        fpath_json=fpath_json,
                        debug=debug,
                    )

                if Path(fpath_yaml).suffix in (".yml", ".yaml"):
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

                if trace_args.lower() in LOG_LEVELS:
                    trace_arg_lineage(
                        f,
                        _change_ledger,
                        level=trace_args,
                    )

                elif trace_args != "":
                    warn(
                        f"'trace_args' has been set to '{trace_args}', which is not supported. Only {LOG_LEVELS} are supported."
                    )

                elif trace_args == "":
                    # default behavior
                    pass

                else:
                    raise ValueError(
                        f"'trace_args' must be set to either one of '{LOG_LEVELS} or an empty string."
                    )

                return f(*_args, **_threshold_kwargs)

            return wrapped_f

        return wrapped
