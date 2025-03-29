from __future__ import annotations

from abc import ABCMeta, abstractmethod
from pathlib import Path

from typing import TypeVar, Any

T = TypeVar("T", dict[str, Any], list[Any], Any)


class BaseModel(metaclass=ABCMeta):
    def __init__(self, model_params: dict[str, Any], templates: Path | None) -> None:
        raise NotImplementedError

    @abstractmethod
    def render(self) -> str: ...


class MixinSerialize:
    @staticmethod
    def _flatten(obj_dict: T) -> T:
        if isinstance(obj_dict, dict):
            flattened_dict = {}
            for key, value in obj_dict.items():
                flattened_dict[key] = MixinSerialize._flatten(value)

            return flattened_dict

        if isinstance(obj_dict, list):
            flattened_list = []
            for item in obj_dict:
                flattened_list.append(MixinSerialize._flatten(item))

            return flattened_list

        if hasattr(obj_dict, "serialize"):
            return obj_dict.serialize()

        return obj_dict

    def serialize(self) -> dict[str, Any]:
        flattened_dict = {}
        for key, value in self.__dict__.items():
            flattened_dict[key] = self._flatten(value)

        return flattened_dict
