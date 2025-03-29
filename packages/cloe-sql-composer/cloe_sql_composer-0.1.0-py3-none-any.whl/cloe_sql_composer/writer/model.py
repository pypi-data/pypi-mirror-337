import logging
import re
from pathlib import Path

from .base import BaseWriter


logger = logging.getLogger(__name__)


class InvalidModelStatementError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class ModelFileWriter(BaseWriter):
    def __init__(self, output: Path) -> None:
        self._output = output
        self._make_dir(self._output)

    def write(self, statement: str) -> None:
        system_pattern = re.compile(r"^system: (?P<system>[a-z]+)$", re.MULTILINE)
        object_pattern = re.compile(
            r"^object_type: (?P<object_type>[a-z_]+)$", re.MULTILINE
        )
        name_pattern = re.compile(r"^name: (?P<name>[A-Za-z0-9_]+)$", re.MULTILINE)
        schema_pattern = re.compile(r"^schema: (?P<schema>[A-Za-z_]+)$", re.MULTILINE)

        match_system = system_pattern.search(statement)
        match_object_type = object_pattern.search(statement)
        match_name = name_pattern.search(statement)
        match_schema = schema_pattern.search(statement)

        if (
            not match_system
            or not match_object_type
            or not match_name
            or not match_schema
        ):
            logger.error("Invalid model statement.")
            raise InvalidModelStatementError("Invalid model statement.")

        system = match_system.group("system")
        object_type = match_object_type.group("object_type")
        name = match_name.group("name")
        schema = match_schema.group("schema")

        object_type += "s"

        p = (
            self._output
            / system.lower()
            / schema.lower()
            / object_type.lower()
            / f"{name.lower()}.yaml"
        )
        self._make_dir(p.parent)

        with p.open("w") as file:
            file.write(statement)
