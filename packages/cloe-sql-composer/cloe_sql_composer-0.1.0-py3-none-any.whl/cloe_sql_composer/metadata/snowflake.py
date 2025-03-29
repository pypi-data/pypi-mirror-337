from __future__ import annotations

import logging
import os
from copy import deepcopy
from typing import Any

from cloe_util_snowflake_connector.connection_parameters import ConnectionParameters
from cloe_util_snowflake_connector.snowflake_interface import SnowflakeInterface

from .base import BaseMetadataLoader
from ..template import MixinTemplateLoader
from .mappings import get_dtype_mapping


logger = logging.getLogger(__name__)


class SnowflakeTableMetadataLoader(MixinTemplateLoader, BaseMetadataLoader):
    def __init__(self, params: dict[str, Any]) -> None:
        sf_interface = SnowflakeInterface(
            ConnectionParameters.init_from_env_variables()
        )

        params["database"] = os.getenv("CLOE_SNOWFLAKE_DATABASE")

        template = self.get_template(
            template_path=None, template_name="query/metadata.sql.j2"
        )
        statement = template.render(**params)

        metadata: list[dict[str, str]] = sf_interface.run_one_with_return(statement)
        self._metadata = self._group_by_table_name(metadata)

        dtype_mapping = params.get("dtype_mapping")
        self._dtype_mapping: dict[str, str] | None
        if dtype_mapping:
            self._dtype_mapping = get_dtype_mapping(**dtype_mapping)
        else:
            self._dtype_mapping = None

    def __getitem__(self, item: str) -> list[dict[str, Any]]:
        table_data = deepcopy(self._metadata[item])

        if self._dtype_mapping:
            for column in table_data:
                column["DATATYPE"] = self._dtype_mapping[column["DATATYPE"].upper()]

        columns: list[dict[str, Any]] = []
        for row in table_data:
            row_dict: dict[str, Any] = {"name": row["COLUMN_NAME"]}
            dtype: str = row["DATATYPE"]

            if dtype.lower() in ("varchar", "date", "boolean", "float"):
                row_dict["datatype"] = dtype.lower()
            elif dtype.lower() == "number":
                row_dict["datatype"] = {
                    "name": "number",
                    "precision": 38,
                    "scale": int(row["SCALE"]),
                }
            elif dtype.lower() in ("time", "timestamp_ntz"):
                row_dict["datatype"] = {
                    "name": dtype.lower(),
                    "precision": int(row["DATE_PRECISION"]),
                }
            else:
                logger.warning(
                    f"Unsupported datatype [ {dtype.lower()} ]. Column will be skipped."
                )
                continue

            row_dict["key"] = row["KEY"]

            columns.append(row_dict)

        return columns

    @staticmethod
    def _group_by_table_name(
        metadata: list[dict[str, str]],
    ) -> dict[str, list[dict[str, str]]]:
        grouped = {}
        for row in metadata:
            tabname = row.pop("TABLE_NAME")
            if tabname not in grouped:
                grouped[tabname] = [row]
            else:
                grouped[tabname].append(row)

        return grouped
