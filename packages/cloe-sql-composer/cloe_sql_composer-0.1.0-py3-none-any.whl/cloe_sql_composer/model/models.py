import logging
from pathlib import Path
from typing import Any

from jinja2.exceptions import TemplateNotFound

from .base import BaseModel, MixinSerialize
from ..template import MixinTemplateLoader
from .column import Column
from ..exceptions import ModelInvalidError


logger = logging.getLogger(__name__)


class TableModel(MixinSerialize, MixinTemplateLoader, BaseModel):
    def __init__(
        self, model_params: dict[str, Any], templates: Path | None = None
    ) -> None:
        try:
            self.table_name = model_params["name"]
            self.schema = model_params["schema"]
            self.columns = self._get_columns(model_params["columns"])
        except KeyError as err:
            logger.error("Model is invald.")
            raise ModelInvalidError("Model is invald.") from err
        except ModelInvalidError as err:
            logger.error("Model is invalid.")
            raise ModelInvalidError("Model is invalid.") from err

        self.prefix = model_params.get("prefix", "TBL")

        template_name = f"{model_params['system']}/{model_params['object_type']}.sql.j2"

        try:
            self.template = self.get_template(templates, template_name)
        except TemplateNotFound as err:
            logger.error(f"Template [ {template_name} ] not found.")
            raise err

    def render(self) -> str:
        return self.template.render(**self.serialize())

    @staticmethod
    def _get_columns(column_params: list[dict[str, Any]]) -> list[Column]:
        columns = []
        for params in column_params:
            columns.append(Column(params))

        return columns


class ProcedureModel(MixinSerialize, MixinTemplateLoader, BaseModel):
    def __init__(
        self, model_params: dict[str, Any], templates: Path | None = None
    ) -> None:
        try:
            self.schema = model_params["schema"]
            self.columns = self._get_columns(model_params["columns"])
        except KeyError as err:
            logger.error("Model is invald.")
            raise ModelInvalidError("Model is invald.") from err
        except ModelInvalidError as err:
            logger.error("Model is invalid.")
            raise ModelInvalidError("Model is invalid.") from err

        prefix = {"prefix": "TBL"}
        self.source = model_params["source"]
        self.source = prefix | self.source

        self.target = model_params["target"]
        self.target = prefix | self.target

        self.prefix = model_params.get("prefix", "SP")

        self.bk = model_params.get("bk")

        template_name = f"{model_params['system']}/{model_params['object_type']}.sql.j2"

        try:
            self.template = self.get_template(templates, template_name)
        except TemplateNotFound as err:
            logger.error(f"Template [ {template_name} ] not found.")
            raise err

    def render(self) -> str:
        return self.template.render(**self.serialize())

    def _get_columns(
        self, column_params: list[str | dict[str, str]]
    ) -> list[tuple[str, str]]:
        column_list: list[tuple[str, str]] = []
        for column in column_params:
            if isinstance(column, str):
                column_list.append((column, column))
            else:
                column_list.append((column["source_name"], column["target_name"]))

        return column_list
