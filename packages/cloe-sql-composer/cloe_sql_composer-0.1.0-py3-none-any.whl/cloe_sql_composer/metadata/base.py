from abc import ABCMeta, abstractmethod
from typing import Any


class BaseMetadataLoader(metaclass=ABCMeta):
    @abstractmethod
    def __getitem__(self, item: str) -> list[dict[str, Any]]: ...
