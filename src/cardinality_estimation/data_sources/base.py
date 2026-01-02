from abc import ABC, abstractmethod
from typing import Iterable


class DataStreamSource(ABC):
    @abstractmethod
    def __iter__(self) -> Iterable[str]:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass