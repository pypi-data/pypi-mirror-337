from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jinja2 import Template as JinjaTemplate

from jinja2 import PackageLoader, FileSystemLoader
from jinja2.environment import Environment


class MixinTemplateLoader:
    @staticmethod
    def get_template(template_path: Path | None, template_name: str) -> JinjaTemplate:
        loader: FileSystemLoader | PackageLoader
        if template_path is None:
            loader = PackageLoader(__name__, "jinja_templates")
        else:
            loader = FileSystemLoader(template_path)

        env = Environment(loader=loader, keep_trailing_newline=True)

        return env.get_template(template_name)
