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
    pass


if __name__ == "__main__":
    main()
