import os
from dataclasses import dataclass
from ..utils import logger

@dataclass(frozen=True)
class Settings:
    timer: tuple | None = None
    root_dir: str | None = None
    size: int | None = None
    format_: str | None = None
    is_valid: bool = False


class SettingsLoader:

    def __init__(self) -> None:
        self.settings_dir = {}

    @staticmethod
    def _load_env_timer(var: str = "TIMER") -> tuple | None:
        timer = os.getenv(var, "1,2")
        timer=timer.split(",")
        timer = [int(t) if t.isnumeric() else 0 for t in timer]
        return (timer[0], timer[1]) if timer else None

    @staticmethod
    def _load_env_root_dir(var: str = "ROOT_DIR") -> str:
        root_dir = os.getenv(var, "results")
        if not root_dir:
            return "results"
        return root_dir

    @staticmethod
    def _load_env_size(var: str = "SIZE") -> int:
        size = os.getenv(var, 5)
        return size if isinstance(size, int) else None

    @staticmethod
    def _load_env_format(var: str = "FORMAT") -> str:
        format_ = os.getenv(var, "FORMAT")
        if format_ and format_.lower().strip() in ["csv", "json"]:
            return format_.lower().strip()
        return "csv"

    def _validate_settings(self) -> bool:
        validation = []

        if isinstance(self.settings_dir["timer"], tuple):
            validation.append(True)

        if isinstance(self.settings_dir["root_dir"], str):
            validation.append(True)

        if isinstance(self.settings_dir["size"], int):
            validation.append(True)

        if isinstance(self.settings_dir["format_"], str):
            validation.append(True)

        return len(validation) == 4


    def load_settings(self) -> Settings:
        self.settings_dir = {
            "timer": self._load_env_timer(),
            "root_dir": self._load_env_root_dir(),
            "size": self._load_env_size(),
            "format_": self._load_env_format(),
        }

        is_valid = self._validate_settings()
        self.settings_dir["is_valid"] = is_valid

        return Settings(**self.settings_dir)

def load_settings() -> Settings | None:
    logger.info("LOADING SETTINGS ...")
    loader = SettingsLoader()
    settings = loader.load_settings()

    logger.info("LOADING SETTINGS ...")
    if not settings.is_valid:
        logger.error("SETTINGS NOT VALID REVIEW ENV VARIABLES")
    else:
        logger.info("SETTINGS OK")
        logger.info(f"  TIMER: {settings.timer}")
        logger.info(f"  ROOT_DIR: {settings.root_dir}")
        logger.info(f"  SIZE: {settings.size}")
        logger.info(f"  FORMAT: {settings.format_}")

    return settings


