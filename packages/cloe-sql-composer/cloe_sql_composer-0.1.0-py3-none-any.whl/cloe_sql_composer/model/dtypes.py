from .base import MixinSerialize


class BaseDataType(MixinSerialize):
    def __init__(self, **kwargs: str):
        self.dtype = kwargs["dtype"]


class DtypeVarchar(BaseDataType):
    def __init__(self, length: int = 16777216, **kwargs: str) -> None:
        super().__init__(dtype="VARCHAR")
        self.length = length


class DtypeNumber(BaseDataType):
    def __init__(self, precision: int = 38, scale: int = 0, **kwargs: str) -> None:
        super().__init__(dtype="NUMBER")
        self.precision = precision
        self.scale = scale


class DtypeFloat(BaseDataType):
    def __init__(self, **kwargs: str) -> None:
        super().__init__(dtype="FLOAT")


class DtypeBoolean(BaseDataType):
    def __init__(self, **kwargs: str) -> None:
        super().__init__(dtype="BOOLEAN")


class DtypeDate(BaseDataType):
    def __init__(self, **kwargs: str) -> None:
        super().__init__(dtype="DATE")


class DtypeTime(BaseDataType):
    def __init__(self, precision: int = 9, **kwargs: str) -> None:
        super().__init__(dtype="TIME")
        self.precision = precision


class DtypeTimeStamp(BaseDataType):
    def __init__(self, precision: int = 9, **kwargs: str) -> None:
        super().__init__(dtype="TIMESTAMP_NTZ")
        self.precision = precision
