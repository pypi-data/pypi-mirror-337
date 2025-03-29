"""Implement SQL writer classes."""

import logging
import re
from pathlib import Path

from .base import BaseWriter


logger = logging.getLogger(__name__)


class InvalidSqlStatmentError(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)


class SqlFileWriter(BaseWriter):
    def __init__(self, output: Path) -> None:
        self._output = output
        self._make_dir(self._output)

    def write(self, statement: str) -> None:
        pattern = re.compile(
            r"CREATE OR REPLACE (?P<object_type>EXTERNAL TABLE|TABLE|PROCEDURE) \"?(?P<schema>[A-Za-z][A-Za-z0-9_]*)\"?\.\"?(?P<object_name>[A-Za-z0-9_]+)\"?"
        )
        object_pattern = re.compile(r"(([A-Z])([A-Z]+))+")

        match = pattern.search(statement)

        if not match:
            logger.error("Invalid SQL statement or unsupported object type.")
            logger.info(
                "Supported object types are: 'TABLE', 'EXTERNAL TABLE', 'PROCEDURE'."
            )
            raise InvalidSqlStatmentError(
                'Invalid SQL statement. Statement must start with "CREATE OR REPLACE <object_type> <schem>.<object_name>".'
            )

        type_ = match.group("object_type")
        schema = match.group("schema")
        object_name = match.group("object_name")

        object_type = ""
        for part in object_pattern.finditer(type_):
            object_type += part.group(2) + part.group(3).lower()

        object_type += "s"

        p = self._output / schema / object_type / f"{schema}.{object_name}.sql"
        self._make_dir(p.parent)

        with p.open("w") as file:
            file.write(statement)
