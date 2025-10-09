import sys

from loguru import logger as LOGGER

from pyprogram_threshold import threshold

LOGGER.remove()


@threshold(
    fpath_json="./threshold.json",
    fpath_yaml="./threshold.yaml",
    cli_pattern="--([A-Za-z_-]+)=([0-9A-Za-z_-]+)",
    trace_args="WARNING",
)
def main(food: str, color: str, age: int, country: str, **kwargs):
    LOGGER.add(sys.stderr, level="INFO")
    LOGGER.info("Welcome to main!")
    LOGGER.info(f"{food=}")
    LOGGER.info(f"{color=}")
    LOGGER.info(f"{age=}")
    LOGGER.info(f"{country=}")
    LOGGER.info(f"{kwargs=}")
    for k, v in kwargs.items():
        LOGGER.info(f"{k=} {v=}")


if __name__ == "__main__":
    main()
