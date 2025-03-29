from abc import ABCMeta, abstractmethod
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class BaseWriter(metaclass=ABCMeta):
    @staticmethod
    def _make_dir(path: Path) -> None:
        if not path.exists():
            logger.info(f"Creating output directory [ {path} ].")
            path.mkdir(parents=True)

    @abstractmethod
    def write(self, statement: str) -> None: ...
