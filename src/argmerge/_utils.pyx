"""Module for utility functions."""
import ast

from loguru import logger as LOGGER

cpdef extract_literals(s: str):
    try:
        return ast.literal_eval(s)
    except Exception as e:
        LOGGER.debug(e)
        return s