"""Module for utility functions."""
import ast


cpdef extract_literals(s: str):
    try:
        return ast.literal_eval(s)
    except Exception:
        return s