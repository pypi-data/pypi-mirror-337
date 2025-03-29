from __future__ import annotations

import logging
from collections.abc import Iterator
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict, Required, Any

import yaml

from ..metadata import SnowflakeTableMetadataLoader
from ..template import MixinTemplateLoader

if TYPE_CHECKING:
    from ..metadata.base import BaseMetadataLoader

logger = logging.getLogger(__name__)


class InvalidConfigError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ConfigItemModel(TypedDict, total=False):
    object_type: Required[str]
    name: Required[str]
    schema: Required[str]
    prefix: str | None


@dataclass
class ConfigItem(MixinTemplateLoader):
    system: str
    object_type: str

    name: str
    schema: str

    metadata_loader: BaseMetadataLoader

    prefix: str | None = None

    def model(self) -> str:
        if self.object_type == "table":
            template = self.get_template(None, "models/table.yaml.j2")
        else:
            raise InvalidConfigError(
                f"Invalid config file. Object type [ {self.object_type} ] is not supported."
            )

        template_params: dict[str, Any] = {
            "system": self.system,
            "object_type": self.object_type,
            "name": self.name,
            "schema": self.schema,
        }

        if self.prefix:
            template_params["prefix"] = self.prefix

        template_params["columns"] = self.metadata_loader[self.name]

        return template.render(**template_params)


@dataclass
class SnowflakeExternalTableConfigItem(ConfigItem):
    location: str | None = None
    file_format: str | None = None


@dataclass
class ProcedureConfigItem(ConfigItem):
    source: dict[str, str] | None = None
    target: dict[str, str] | None = None

    def model(self) -> str:
        if self.object_type == "procedure":
            template = self.get_template(None, "models/procedure.yaml.j2")
        else:
            raise InvalidConfigError(
                f"Invalid config file. Object type [ {self.object_type} ] is not supported."
            )

        template_params: dict[str, Any] = {
            "system": self.system,
            "object_type": self.object_type,
            "name": self.name,
            "schema": self.schema,
        }

        source_default = {
            "name": self.name,
            "schema": self.schema,
        }

        if self.source is None:
            self.source = source_default
        else:
            self.source = source_default | self.source

        target_default = {
            "name": self.name,
            "schema": self.schema,
        }

        if self.target is None:
            self.target = target_default
        else:
            self.target = target_default | self.target

        if self.prefix:
            template_params["prefix"] = self.prefix

        template_params["source"] = self.source
        template_params["target"] = self.target

        template_params["columns"] = self.metadata_loader[self.name]

        return template.render(**template_params)


class Config(Iterator[ConfigItem]):
    _keywords = ["metadata", "system", "object_type", "schema", "objects"]
    _supported_systems_objects = {
        "snowflake": {
            "object_types": ["table", "external_table", "procedure"],
            "additional_keywords": [
                "location",
                "file_format",
                "prefix",
                "source",
                "target",
            ],
        }
    }

    def __init__(self, filename: Path):
        self._next = 0

        config_dict = yaml.safe_load(filename.read_text())

        try:
            self._metadata = self._get_metadata_loader(config_dict.pop("metadata"))
        except KeyError as err:
            logger.error("Invalid config file. Missing key: [ 'metadata' ].")
            raise InvalidConfigError(
                "Invalid config file. Missing key: [ 'metadata' ]."
            ) from err

        try:
            self._system = config_dict.pop("system").lower()
        except KeyError as err:
            logger.error("Invalid config file. Missing key: [ 'system' ].")
            raise InvalidConfigError(
                "Invalid config file. Missing key: [ 'system' ]."
            ) from err

        if self._system not in self._supported_systems_objects:
            logger.error(
                f"Invalid config file. System [ '{self._system}' ] is not supported.']"
            )
            raise InvalidConfigError(
                f"Invalid config file. System [ '{self._system}' ] is not supported."
            )

        global_params, groups = self._get_group_parameters(config_dict)

        self._config_items: list[ConfigItem] = []
        for group_name, group in groups.items():
            cp_group = deepcopy(group)
            try:
                objects = cp_group.pop("objects")
            except KeyError as err:
                logger.error(
                    f"Invalid config file. Group [ '{group_name}' ] is invalid."
                )
                raise InvalidConfigError(
                    f"Invalid config file. Group [ '{group_name}' ] is invalid."
                ) from err

            for obj in objects:
                params = deepcopy(global_params)
                cp_obj = deepcopy(obj)

                params |= cp_group
                params |= cp_obj

                try:
                    object_type = params["object_type"]
                except KeyError as err:
                    logger.error(
                        f"Invalid config file. Group [ '{group_name}' ] is invalid."
                    )
                    raise InvalidConfigError(
                        f"Invalid config file. Group [ '{group_name}' ] is invalid."
                    ) from err

                if (
                    object_type
                    not in self._supported_systems_objects[self._system]["object_types"]
                ):
                    logger.error(
                        f"Invalid config file. Object type [ '{object_type}' ] is not supported."
                    )
                    raise InvalidConfigError(
                        f"Invalid config file. Object type [ '{object_type}' ] is not supported."
                    )

                self._config_items.append(self._item_factory(params, object_type))

    def __next__(self) -> ConfigItem:
        if self._next == len(self._config_items):
            raise StopIteration

        item = self._config_items[self._next]
        self._next += 1

        return item

    @staticmethod
    def _get_metadata_loader(metadata: dict[str, Any]) -> BaseMetadataLoader:
        if metadata["type"] == "snowflake_table":
            return SnowflakeTableMetadataLoader(metadata)

        logger.error(
            f"Invalid config file. Type [{metadata['type']}] is not supported."
        )
        raise InvalidConfigError(
            f"Unsupported metadata loader. Type [ '{metadata['type']}' ] is not supported.' ]"
        )

    @staticmethod
    def _get_global_parameters(
        config_dict: dict[str, Any], keywords: list[str]
    ) -> dict[str, str]:
        global_params = {}

        for key in keywords:
            if key == "objects":
                continue

            try:
                global_params[key] = config_dict.pop(key)
            except KeyError:
                continue

        return global_params

    def _get_group_parameters(
        self, config_dict: dict[str, Any]
    ) -> tuple[dict[str, str], dict[str, dict[str, Any]]]:
        keywords = deepcopy(self._keywords)
        keywords.extend(
            self._supported_systems_objects[self._system]["additional_keywords"]
        )

        global_params = self._get_global_parameters(config_dict, keywords)

        groups = {}
        if "objects" in config_dict:
            groups["default"] = {"objects": config_dict.pop("objects")}

        if not groups:
            for k, v in config_dict.items():
                groups[k] = {}

                for key in keywords:
                    try:
                        groups[k][key] = v[key]
                    except KeyError:
                        continue

        if not groups:
            logger.error("Invalid config file. Group [ 'default' ] is invalid.")
            raise InvalidConfigError(
                "Invalid config file. Group [ 'default' ] is invalid."
            )

        return global_params, groups

    def _item_factory(self, params: dict[str, Any], object_type: str) -> ConfigItem:
        item: ConfigItem
        if self._system == "snowflake" and object_type == "external_table":
            item = SnowflakeExternalTableConfigItem(
                **params, system=self._system, metadata_loader=self._metadata
            )
        elif self._system == "snowflake" and object_type == "procedure":
            item = ProcedureConfigItem(
                **params, system=self._system, metadata_loader=self._metadata
            )
        else:
            item = ConfigItem(
                **params, system=self._system, metadata_loader=self._metadata
            )

        return item
