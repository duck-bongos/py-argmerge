from abc import ABC

__all__ = ["SourceParser"]


class SourceParser(ABC):
    rank: int
    label: str

    def __init__(self, rank: int, label: str):
        self.rank = rank
        self.label = label

    def __call__(
        cls, threshold_kwargs: dict, ledger: dict, debug: bool = False, **kwargs
    ):
        raise NotImplementedError
