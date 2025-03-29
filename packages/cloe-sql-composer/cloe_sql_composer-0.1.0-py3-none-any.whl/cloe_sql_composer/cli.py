import logging
from pathlib import Path
from typing import Annotated, Optional

import typer
from dotenv import load_dotenv

from .config import Config
from .loader import ModelLoader
from .writer import SqlFileWriter, ModelFileWriter

app = typer.Typer(pretty_exceptions_show_locals=False)

logger = logging.getLogger(__name__)


@app.command()
def model(
    filename: Annotated[
        Path,
        typer.Argument(
            help=(
                "Configuration YAML file providing the necessary "
                "information for the model creation."
            )
        ),
    ],
    output: Annotated[
        Path,
        typer.Option(help="Root directory to store the generated YAML model files."),
    ] = Path("./models"),
    env: Annotated[
        Optional[Path],
        typer.Option(help="Path to file storing additional environment variables."),
    ] = None,
) -> None:
    if not filename.is_file():
        logger.error(f"File {filename} does not exist.")
        raise typer.Exit(1)

    if env and not env.is_file():
        logger.error(f"File {env} does not exist.")
        raise typer.Exit(1)

    if env:
        load_dotenv(env)

    config = Config(filename)
    writer = ModelFileWriter(output)
    for item in config:
        result = item.model()
        writer.write(result)


@app.command()
def sql(
    models: Annotated[
        Path, typer.Argument(help="Path to model repository or single model.")
    ],
    output: Annotated[
        Path, typer.Option(help="Root directory to store generated SQL statements.")
    ] = Path("./sql_output"),
    templates: Annotated[
        Optional[Path],
        typer.Option(help="Root of template repo with custom Jinja templates."),
    ] = None,
) -> None:
    if not models.exists():
        logger.error(f"Model(s) [ {models} ] not found.")
        raise typer.Exit(1)

    if templates:
        if templates.exists():
            if templates.is_file():
                logger.error(
                    "Provide folder path with custom templates "
                    "and not a single template file."
                )
                raise typer.Exit(1)
        else:
            logger.error(f"Templates [ {templates} ] not found.")
            raise typer.Exit(1)

    writer = SqlFileWriter(output)
    models_loaded = ModelLoader(models, templates)

    for model in models_loaded:
        statement = model.render()
        writer.write(statement)


def main() -> None:
    app()
