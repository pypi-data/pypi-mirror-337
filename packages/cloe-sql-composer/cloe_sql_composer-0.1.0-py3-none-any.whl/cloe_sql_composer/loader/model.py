import logging
import os
from collections.abc import Iterator
from enum import Enum
from pathlib import Path
from typing import Any

import yaml

from ..exceptions import ModelInvalidError
from ..model.base import BaseModel
from ..model.models import TableModel, ProcedureModel

logger = logging.getLogger(__name__)


class SnowflakeSupportedModels(Enum):
    table = TableModel
    procedure = ProcedureModel


class SupportedSystems(Enum):
    snowflake = SnowflakeSupportedModels


class ModelLoader(Iterator[BaseModel]):
    def __init__(self, modelpath: Path, templates: Path | None = None) -> None:
        if not modelpath.exists():
            logger.error(f"[ {modelpath} ] not found.")
            raise FileNotFoundError("No such file or directory")

        if templates and not templates.exists():
            logger.error(f"[ {templates} ] not found.")
            raise FileNotFoundError("No such file or directory")

        self._next = 0
        self._templates = templates

        self._models: list[BaseModel] = []
        if modelpath.is_file():
            self._models.append(self._load_model(modelpath))
        else:
            for dirpath, _, filenames in os.walk(modelpath.resolve()):
                if filenames:
                    dp = Path(dirpath)
                    for filename in filenames:
                        self._models.append(self._load_model(dp / filename))

    def __next__(self) -> BaseModel:
        if len(self._models) == self._next:
            raise StopIteration

        m = self._models[self._next]
        self._next += 1

        return m

    def _load_model(self, file: Path) -> BaseModel:
        model_dict: dict[str, Any] = yaml.safe_load(file.open())

        try:
            target_system = model_dict["system"]
        except KeyError as err:
            logger.error(f"Model [ {file} ] is invalid. Key [ system ] is missing.")
            raise ModelInvalidError("Model is invalid.") from err

        try:
            object_type = model_dict["object_type"]
        except KeyError as err:
            logger.error(
                f"Model [ {file} ] is invalid. Key [ object_type ] is missing."
            )
            raise ModelInvalidError("Model is invalid.") from err

        try:
            system_enum = getattr(SupportedSystems, target_system).value
        except AttributeError as err:
            logger.error(f"System [ {target_system} ] is not supported.")
            raise ModelInvalidError(
                f"System [ {target_system} ] is not supported."
            ) from err

        try:
            model: type[BaseModel] = getattr(system_enum, object_type).value
        except AttributeError as err:
            logger.error(f"Object type [ {object_type} ] is not supported.")
            raise ModelInvalidError(
                "Object type [ function ] is not supported."
            ) from err

        return model(model_dict, self._templates)
