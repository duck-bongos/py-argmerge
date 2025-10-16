# Example Usage
Below, we'll show you how to display the keywords from each source, how to bypass using the `threshold` decorator entirely, then walk through examples that build on each other to show how arguments are overwritten.

## Tracing
We added the ability to trace the source of each keyword argument. We set this using `threshold`'s kwarg `trace_level`. `trace_level` uses the [`loguru` package for logging](https://github.com/Delgan/loguru) and accepts the following arguments (case insenitive): 

- `"critical"`
- `"warning"`
- `"success"`
- `"info"`
- `"debug"`

We will see how this is used by trying out different log levels in the next set of examples.

## Developer-Provided Arguments (Highest Level)
If you need to debug something _really_ quickly and don't want to fuss around with files or CLI, you can pass the values in **as keywords**. This bypasses any external values provided from files, environment variables, or the CLI.
```py
# main.py
from argmerge import threshold


@threshold(trace_level="DEBUG")
def main(first, second, third: float = 3.0, fourth: float = 4.0, fifth: int = 5):
    print(
        f"{first=}",
        f"{second=}",
        f"{third=}",
        f"{fourth=}",
        f"{fifth=}",
        sep="\n",
    )


if __name__ == "__main__":
    main(first=1, second="second")

```
Outputs a list of keyword arguments with their sources listed in ascending priority order
```sh
$ uv run main.py
2025-10-15 21:08:02.681 | DEBUG    | argmerge.trace:_write_trace:51 - 
Parameter Name  | Source                 
=======================================
third   | Python Function Default
fourth  | Python Function Default
fifth   | Python Function Default
first   | Developer-provided     
second  | Developer-provided     
=======================================
first=1
second='second'
third=3.0
fourth=4.0
fifth=5
```


## Default Function Values (Lowest Level)
```py
# main.py
from argmerge import threshold


@threshold(trace_level="DEBUG")
def main(
    first: int = 1,
    second: str = "second",
    third: float = 3.0,
    fourth: float = 4.0,
    fifth: int = 5,
):
    print(
        f"{first=}",
        f"{second=}",
        f"{third=}",
        f"{fourth=}",
        f"{fifth=}",
        sep="\n",
    )


if __name__ == "__main__":
    main()
```
Output
```sh
$ uv run main.py
2025-10-15 21:19:07.874 | DEBUG    | argmerge.trace:_write_trace:51 - 
Parameter Name  | Source                 
=======================================
first   | Python Function Default
second  | Python Function Default
third   | Python Function Default
fourth  | Python Function Default
fifth   | Python Function Default
=======================================
first=1
second='second'
third=3.0
fourth=4.0
fifth=5
```

## JSON (Second Lowest)
JSON Config
```json
// threshold.json
{
    "first": 100,
    "second": "Python"
}
```
```py
# main.py
from argmerge import threshold


@threshold(fpath_json="threshold.json", trace_level="DEBUG")
def main(
    first: int,
    second: str,
    third: float = 3.0,
    fourth: float = 4.0,
    fifth: int = 5,
):
    print(
        f"{first=}",
        f"{second=}",
        f"{third=}",
        f"{fourth=}",
        f"{fifth=}",
        sep="\n",
    )


if __name__ == "__main__":
    main()
```
Outputs
```sh
$ uv run main.py
2025-10-15 21:19:36.388 | DEBUG    | argmerge.trace:_write_trace:51 - 
Parameter Name  | Source                 
=======================================
third   | Python Function Default
fourth  | Python Function Default
fifth   | Python Function Default
first   | JSON (threshold.json)  
second  | JSON (threshold.json)  
=======================================
first=100
second='Python'
third=3.0
fourth=4.0
fifth=5 
```


## YAML (Third Lowest)
```yaml
# threshold.yaml
third: -3.333
```
```py
# main.py
from argmerge import threshold


@threshold(
    fpath_json="threshold.json", 
    fpath_yaml="threshold.yaml", 
    trace_level="DEBUG"
)
def main(
    first: int,
    second: str,
    third: float = 3.0,
    fourth: float = 4.0,
    fifth: int = 5,
):
    print(
        f"{first=}",
        f"{second=}",
        f"{third=}",
        f"{fourth=}",
        f"{fifth=}",
        sep="\n",
    )


if __name__ == "__main__":
    main()
```
Output
```sh
$ uv run main.py
2025-10-15 21:24:21.619 | DEBUG    | argmerge.trace:_write_trace:51 - 
Parameter Name  | Source                 
=======================================
fourth  | Python Function Default
fifth   | Python Function Default
first   | JSON (threshold.json)  
second  | JSON (threshold.json)  
third   | YAML (threshold.yaml)  
=======================================
first=100
second='Python'
third=-3.333
fourth=4.0
fifth=5
```

## Environment Variables (Third Highest)
```sh
$ export EXAMPLE_THRESH_FOURTH=-14.0
```
```py
# main.py
from argmerge import threshold


@threshold(
    fpath_json="threshold.json",
    fpath_yaml="threshold.yaml",
    env_prefix="EXAMPLE_THRESH",
    trace_level="WARNING",
)
def main(
    first: int,
    second: str,
    third: float = 3.0,
    fourth: float = 4.0,
    fifth: int = 5,
):
    print(
        f"{first=}",
        f"{second=}",
        f"{third=}",
        f"{fourth=}",
        f"{fifth=}",
        sep="\n",
    )


if __name__ == "__main__":
    main()
```
Outputs
```sh
$ uv run main.py
2025-10-15 21:26:37.188 | DEBUG    | argmerge.trace:_write_trace:51 - 
Parameter Name  | Source                 
=======================================
fifth   | Python Function Default
first   | JSON (threshold.json)  
second  | JSON (threshold.json)  
third   | YAML (threshold.yaml)  
fourth  | Environment Variable   
=======================================
first=100
second='Python'
third=-3.333
fourth=-14.0
fifth=5 
```

## Command-Line Arguments (Second Highest)

```py
# main.py
from argmerge import threshold


@threshold(
    fpath_json="threshold.json",
    fpath_yaml="threshold.yaml",
    env_prefix="EXAMPLE_THRESH",
    cli_pattern=r"--([A-Za-z_-]+)=([0-9A-Za-z._-]+)",  # the default pattern
    trace_level="WARNING",
)
def main(
    first: int,
    second: str,
    third: float = 3.0,
    fourth: float = 4.0,
    fifth: int = 5,
):
    print(
        f"{first=}",
        f"{second=}",
        f"{third=}",
        f"{fourth=}",
        f"{fifth=}",
        sep="\n",
    )


if __name__ == "__main__":
    main()
```

Output
```sh
$ uv run main.py -- --fifth=3.14
$ # you can also run
$ # python main.py --fifth=3.14
2025-10-15 21:28:51.405 | DEBUG    | argmerge.trace:_write_trace:51 - 
Parameter Name  | Source               
=====================================
first   | JSON (threshold.json)
second  | JSON (threshold.json)
third   | YAML (threshold.yaml)
fourth  | Environment Variable 
fifth   | CLI                  
=====================================
first=100
second='Python'
third=-3.333
fourth=-14.0
fifth='3.14'   
```