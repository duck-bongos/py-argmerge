from argmerge import threshold


@threshold(
    fpath_json="threshold.json",
    fpath_yaml="threshold.yaml",
    env_prefix="EXAMPLE_THRESH",
    trace_level="DEBUG",
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
