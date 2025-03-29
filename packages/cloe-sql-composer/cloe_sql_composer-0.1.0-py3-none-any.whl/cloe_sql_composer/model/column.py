from __future__ import annotations

import logging
from copy import deepcopy
from enum import Enum
from typing import TYPE_CHECKING, Any

from ..exceptions import ModelInvalidError
from .base import MixinSerialize
from .dtypes import (
    DtypeTime,
    DtypeDate,
    DtypeFloat,
    DtypeVarchar,
    DtypeBoolean,
    DtypeNumber,
    DtypeTimeStamp,
)

if TYPE_CHECKING:
    from .dtypes import BaseDataType

logger = logging.getLogger(__name__)


class Column(MixinSerialize):
    class DatatypeMapping(Enum):
        varchar = DtypeVarchar
        number = DtypeNumber
        float = DtypeFloat
        boolean = DtypeBoolean
        date = DtypeDate
        time = DtypeTime
        timestamp = DtypeTimeStamp

    class DefaultValues(Enum):
        varchar = "#"
        number = 0
        float = 0
        boolean = False
        date = "1900-01-01"
        time = "00:00:00"
        timestamp = "1900-01-01"

    def __init__(self, column_params: dict[str, Any]) -> None:
        try:
            self.name = column_params["name"]
            self.datatype = self._get_datatype(column_params["datatype"])
        except KeyError as err:
            logger.error("Model is invalid.")
            raise ModelInvalidError("Model is invalid.") from err
        except AttributeError as err:
            logger.error("Unsupported datatype.")
            raise ModelInvalidError("Unsupported datatype.") from err

        self.key = column_params.get("key", False)
        self.nullable = column_params.get("nullable", True)

        try:
            self.default = self._get_default(column_params.get("default"))
        except AttributeError as err:
            logger.error("Model is invalid.")
            raise ModelInvalidError("Model is invalid.") from err

        if self.key or self.default:
            self.nullable = False

    def _get_datatype(self, params: str | dict[str, str]) -> BaseDataType:
        params_copy = deepcopy(params)
        if isinstance(params_copy, str):
            dtype = params_copy.lower()
            params_copy = {"dtype": dtype}
        else:
            dtype = params_copy["name"].lower()

        dtype_cls: type[BaseDataType] = getattr(self.DatatypeMapping, dtype).value

        return dtype_cls(**params_copy)

    def _get_default(self, default: Any) -> Any:
        if self.datatype.dtype is None:
            raise ModelInvalidError("Model is invalid.")

        if default is None and (self.key or not self.nullable):
            default = getattr(self.DefaultValues, self.datatype.dtype.lower()).value

        return default
