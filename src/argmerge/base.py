from abc import ABC, abstractmethod

__all__ = ["SourceParser"]


class SourceParser(ABC):
    rank: int = -100
    label: str = ""

    def __init__(cls):
        cls.label
        cls.rank

    @abstractmethod
    def __call__(
        cls, threshold_kwargs: dict, ledger: dict, debug: bool = False, **kwargs
    ) -> tuple[dict, dict]:
        """This is too abstract to be covered"""
